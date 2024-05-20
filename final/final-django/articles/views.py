import os
import numpy as np
import cv2
import tensorflow as tf
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.contrib.auth.decorators import login_required
from tensorflow.keras.models import load_model
from .models import *
from .serializers import PostSerializer, CommentSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from django.contrib.auth import get_user_model
from rest_framework import status
from django.shortcuts import get_object_or_404
import json
import requests
import json
import urllib
from PIL import Image
from googletrans import Translator


# 배우 리스트
actors = ['김다미', '김수현', '김우빈', '김지원', '김태리', '김혜수', '김혜윤', '마동석', '박보영', '박서준', '박신혜', '박은빈', '손석구',
          '손예진', '송강호', '송중기', '송혜교', '수지', '신세경', '유승호', '유해진', '윤아', '이도현', '이동휘', '이병헌', '이세영', '이정재', '이주빈', '임시완', '전도연']

# 모델 파일 경로
MODEL_PATH = os.path.abspath('C:/Users/SSAFY/Desktop/sinijini/fin_pjt/Web-pages-utilizing-movie-data/final/final-django/articles/CNN/model.h5')
print(MODEL_PATH)
model = load_model(MODEL_PATH)
REST_API_KEY = '8f7951c8882033e6548aa0bd67a0f772'
# 얼굴 탐지 모델 로드
face_cascade = cv2.CascadeClassifier('C:/Users/SSAFY/Desktop/sinijini/fin_pjt/Web-pages-utilizing-movie-data/final/final-django/articles/haarcascade_frontalface_default.xml')
print(face_cascade)
# 이미지 전처리 함수
def preprocess_image(image):
    image = cv2.resize(image, (35, 35))
    image = image.astype("float") / 255.0
    # print('전처리 완료')
    return image

@api_view(['POST'])
def find_similar_actor(request):
    if request.method == 'POST':
        image_file = request.FILES['image']
        
        # 이미지를 읽어와서 전처리
        image = cv2.imdecode(np.frombuffer(image_file.read(), np.uint8), cv2.IMREAD_COLOR)
        
        # 얼굴 탐지
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        if len(faces) == 0:
            return JsonResponse({'error': 'No face detected'})

        x, y, w, h = faces[0]
        cropped = image[y: y + h, x: x + w]
        
        processed_image = preprocess_image(cropped)
        
        # 모델에 전달하여 예측 수행
        # print(processed_image)
        prediction = model.predict(np.expand_dims(processed_image, axis=0))
        
        # 예측 결과에서 가장 높은 확률의 클래스 선택
        # print(prediction)
        predicted_class = np.argmax(prediction)
        
        # 클래스를 배우의 이름으로 변환
        predicted_actor = actors[predicted_class]
        # print(predicted_actor)

        predicted_img = f'final/image/{predicted_class}.jpg'

        return JsonResponse({'similar_actor': predicted_actor, 'img_url':predicted_img})
    
    return JsonResponse({'error': 'POST method required'})




@api_view(['POST'])
def upload_post(request):
    print(request.method)
    if request.method == 'POST':
        # 업로드된 파일과 데이터 처리
        print('여기는 articles의 view함수입니다.')
        print(request.POST)
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')
        if title and content and image:
            # 이미지 저장
            file_path = default_storage.save('uploads/' + image.name, image)
            # 포스트 저장 로직 추가 (예: 데이터베이스에 저장)
            return JsonResponse({'message': 'Post uploaded successfully'})
        return JsonResponse({'error': 'Missing required fields'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)



# 커뮤니티
@csrf_exempt
@api_view(['POST'])
def upload_result(request):
    if request.method == 'POST':
        data = {
                'content': request.POST.get('content'),
                'image': request.POST.get('image'),
                'user': request.user.id
            }
        Post.objects.create(
            content=request.POST.get('content'),
            image= request.POST.get('image'),
            user= request.user
        )
        print()
        return Response(data,status=status.HTTP_201_CREATED)
    return JsonResponse({'error': 'POST method required'}, status=405)




# 커뮤니티
@csrf_exempt
@api_view(['POST'])
def create_post(request):
    if request.method == 'POST':
        print('여기는 create_post')
        print(request.POST.get('content'))
        print(request.FILES['image'])
        print('여기다')
        print(request.user.id)
        data = {
                'content': request.POST.get('content'),
                'image': request.FILES.get('image'),
                'user': request.user.id
            }
        print(data)
        serializer = PostSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            print('여길 통과하지 못한거니?')
            serializer.save(user=request.user)
            print('serializer검증을 했다고....ㅠㅜ')
            print(request.user)
            # post.user = request.user
            # post.save()
            # print(post)
            print('성공했니? 여기는 view의 create_post야')
            return Response( serializer.data,status=status.HTTP_201_CREATED)
        # return JsonResponse({'success': True, 'post_id': post.id, 'image_url': image_url})
    return JsonResponse({'error': 'POST method required'}, status=405)



@api_view(['GET'])
def get_posts(request):
    posts = Post.objects.all().order_by('-created_at')
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)



@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def my_posts(request):
    user = request.user
    posts = Post.objects.filter(user=user).order_by('-created_at')
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def following_posts(request):
    user = request.user
    following = Follow.objects.filter(follower=user).values_list('following_id', flat=True)
    posts = Post.objects.filter(user__in=following).order_by('-created_at')
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)



User = get_user_model()

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def follow_user(request, user_id):
    follower = request.user
    following = get_object_or_404(User, id=user_id)
    if follower != following:
        Follow.objects.get_or_create(follower=follower, following=following)
        return Response({'status': 'followed'}, status=status.HTTP_200_OK)
    return Response({'status': 'cannot follow yourself'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    if post.likes.filter(id=user.id).exists():
        post.likes.remove(user)
        return Response({'status': 'unliked'}, status=status.HTTP_200_OK)
    else:
        post.likes.add(user)
        return Response({'status': 'liked'}, status=status.HTTP_200_OK)


def create_comment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = request.user
        post_id = data.get('post_id')
        text = data.get('text')
        
        post = Post.objects.get(id=post_id)
        comment = Comment.objects.create(user=user, post=post, text=text)
        
        return JsonResponse({'success': True, 'comment_id': comment.id, 'text': comment.text})
    return JsonResponse({'error': 'POST method required'})


@csrf_exempt
@api_view(['POST'])
def GenerateImageView(request):
    if request.method == 'POST':
        keywords = request.POST.getlist('keywords[]')
        res = f'{keywords[3]}인 {keywords[1]}한 {keywords[0]}가 {keywords[5]}에 있는 {keywords[2]}이자 주인공인 {keywords[4]}장르의 영화 포스터인데, {keywords[6]} {keywords[7]}'
        print(res)
        # 프롬프트에 사용할 제시어
        translator = Translator()
        prompt = translator.translate(res,src='ko',dest='en')
        print(prompt.text)
        
        negative_prompt = ""

        # 이미지 생성하기 REST API 호출
        response = t2i(prompt.text, negative_prompt)
        img_url = response.get("images")[0].get("image")
        print(img_url)
        # 응답의 첫 번째 이미지 생성 결과 출력하기
        return JsonResponse({'img_url':img_url})        
    




# 이미지 생성하기 요청
def t2i(prompt, negative_prompt):
    r = requests.post(
        'https://api.kakaobrain.com/v2/inference/karlo/t2i',
        json = {
            "version": "v2.1", 
            "prompt": prompt,
            "negative_prompt": negative_prompt, 
            "height": 1024,
            "width": 1024
        },
        headers = {
            'Authorization': f'KakaoAK {REST_API_KEY}',
            'Content-Type': 'application/json'
        }
    )
    # 응답 JSON 형식으로 변환
    response = json.loads(r.content)
    return response


