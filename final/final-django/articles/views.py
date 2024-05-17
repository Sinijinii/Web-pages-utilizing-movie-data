import os
import numpy as np
import cv2
import tensorflow as tf
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from tensorflow.keras.models import load_model

# 배우 리스트
actors = ['김다미', '김수현', '김우빈', '김지원', '김태리', '김혜수', '김혜윤', '마동석', '박보영', '박서준', '박신혜', '박은빈', '손석구',
          '손예진', '송강호', '송중기', '송혜교', '수지', '신세경', '유승호', '유해진', '윤아', '이도현', '이동휘', '이병헌', '이세영', '이정재', '이주빈', '임시완', '전도연']

# 모델 파일 경로
MODEL_PATH = os.path.abspath('C:/Users/oops5/OneDrive/Desktop/SSAFY/fin_pjt/Web-pages-utilizing-movie-data/final/final-django/articles/CNN/model.h5')
print(MODEL_PATH)
model = load_model(MODEL_PATH)

# 얼굴 탐지 모델 로드
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
print(face_cascade)
# 이미지 전처리 함수
def preprocess_image(image):
    image = cv2.resize(image, (35, 35))
    image = image.astype("float") / 255.0
    print('전처리 완료')
    return image

@csrf_exempt
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
        print(processed_image)
        prediction = model.predict(np.expand_dims(processed_image, axis=0))
        
        # 예측 결과에서 가장 높은 확률의 클래스 선택
        print(prediction)
        predicted_class = np.argmax(prediction)
        
        # 클래스를 배우의 이름으로 변환
        predicted_actor = actors[predicted_class]
        print(predicted_actor)

        predicted_img = f'final/image/{predicted_class}.jpg'

        return JsonResponse({'similar_actor': predicted_actor, 'img_url':predicted_img})
    
    return JsonResponse({'error': 'POST method required'})
