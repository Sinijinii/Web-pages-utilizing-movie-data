import cv2
import requests
import numpy as np
import os
from PIL import Image
import mediapipe as mp

# 이미지 다운로드 함수
def download_image(url, save_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print(f"Image downloaded successfully: {save_path}")
    else:
        print(f"Failed to download image: {url}")
        exit()

# 웹 URL 이미지 다운로드
poster_url = 'https://media.bunjang.co.kr/product/107446052_1_1661554444_w360.jpg'
poster_path = 'poster.jpg'
download_image(poster_url, poster_path)

your_face_url = "https://img.etoday.co.kr/pto_db/2020/11/20201101173437_1533088_504_670.jpg"
your_face_path = 'face.jpg'
download_image(your_face_url, your_face_path)

# 이미지 불러오기
poster_img = cv2.imread(poster_path)
your_face_img = cv2.imread(your_face_path)

# 이미지가 제대로 로드되었는지 확인
if poster_img is None:
    print("Poster image not found.")
    exit()

if your_face_img is None:
    print("Your face image not found.")
    exit()

print("Images loaded successfully.")

# Mediapipe 초기화
mp_face_mesh = mp.solutions.face_mesh
print("여기는?")
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1)
print("여기도??")

# 얼굴 랜드마크 추출 함수
def get_landmarks(img):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(img_rgb)
    if results.multi_face_landmarks:
        landmarks = results.multi_face_landmarks[0]
        return [(lm.x, lm.y) for lm in landmarks.landmark]
    else:
        return None

poster_landmarks = get_landmarks(poster_img)
your_face_landmarks = get_landmarks(your_face_img)

# 랜드마크 검출 확인
if poster_landmarks is None:
    print("Poster face landmarks not found.")
    exit()

if your_face_landmarks is None:
    print("Your face landmarks not found.")
    exit()

print("Landmarks detected successfully.")

# 랜드마크 좌표를 numpy 배열로 변환
poster_landmarks = np.array(poster_landmarks) * [poster_img.shape[1], poster_img.shape[0]]
your_face_landmarks = np.array(your_face_landmarks) * [your_face_img.shape[1], your_face_img.shape[0]]

# 얼굴 교체 함수
def warp_and_blend(face_img, src_landmarks, dst_landmarks, dst_img):
    h, status = cv2.findHomography(src_landmarks, dst_landmarks)
    if h is None:
        print("Homography calculation failed.")
        return dst_img
    
    warped_face = cv2.warpPerspective(face_img, h, (dst_img.shape[1], dst_img.shape[0]))
    
    # 마스크 생성
    mask = np.zeros(dst_img.shape, dtype=dst_img.dtype)
    cv2.fillConvexPoly(mask, np.int32(dst_landmarks), (255, 255, 255))

    # 이미지 블렌딩
    result = cv2.seamlessClone(warped_face, dst_img, mask, (dst_img.shape[1]//2, dst_img.shape[0]//2), cv2.MIXED_CLONE)
    return result

# 얼굴 교체 수행
result_img = warp_and_blend(your_face_img, your_face_landmarks, poster_landmarks, poster_img)

# 결과 저장
output_path = 'output/result.jpg'
cv2.imwrite(output_path, result_img)
print(f"Result image saved successfully: {output_path}")

# 결과 출력
Image.open(output_path).show()
print("Process completed successfully.")
