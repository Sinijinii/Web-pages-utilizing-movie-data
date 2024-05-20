from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import MaxPooling2D, Conv2D, Activation, Dropout, Flatten, Dense
from tensorflow.keras import layers
import numpy as np
import os
import cv2

# 사용자 정의 레이어 클래스
class CustomLayer(layers.Layer):
    def __init__(self, filters, kernel_size, activation, rate=0.1):
        super(CustomLayer, self).__init__()
        self.conv = Conv2D(filters, kernel_size, padding='same')
        self.activation = Activation(activation)
        self.dropout = Dropout(rate)
    
    def call(self, inputs, training=False):
        x = self.conv(inputs)
        x = self.activation(x)
        return self.dropout(x, training=training)
    
    def get_config(self):
        config = super().get_config()
        config.update({
            'filters': self.conv.filters,
            'kernel_size': self.conv.kernel_size,
            'activation': self.activation.get_config()['activation'],
            'rate': self.dropout.rate
        })
        return config

def load_data(train_folder, test_folder):
    train_images = []
    train_labels = []
    test_images = []
    test_labels = []

    # train 이미지 불러오기
    for i in range(1, 31):  # 1부터 30까지의 폴더
        folder_path = os.path.join(train_folder, str(i))
        print(folder_path)
        for filename in os.listdir(folder_path):
            print('------------------------------------')
            print(filename)
            image_path = os.path.join(folder_path, filename)
            print(image_path)
            # 이미지를 읽어와서 numpy 배열로 변환
            image = cv2.imread(image_path)

            image = cv2.resize(image, (35, 35))
            train_images.append(image)
            # 라벨 추가
            train_labels.append(i-1)

    # test 이미지 불러오기
    for i in range(1, 31):  # 1부터 30까지의 폴더
        folder_path = os.path.join(test_folder, str(i))
        for filename in os.listdir(folder_path):
            image_path = os.path.join(folder_path, filename)
            # 이미지를 읽어와서 numpy 배열로 변환
            image = cv2.imread(image_path)

            image = cv2.resize(image, (35, 35))
            test_images.append(image)
            # 라벨 추가
            test_labels.append(i-1)

    return np.array(train_images), np.array(train_labels), np.array(test_images), np.array(test_labels)

# 카테고리 지정하기
nb_classes = 30

# 이미지 크기 지정하기
image_w = 64
image_h = 64

# 데이터 폴더 경로 지정
train_folder = os.path.abspath('Web-pages-utilizing-movie-data/Face-recognition-using-CNN/train_img')
test_folder = os.path.abspath('Web-pages-utilizing-movie-data/Face-recognition-using-CNN/test_img')

# 데이터 열기 
X_train, y_train, X_test, y_test = load_data(train_folder, test_folder)

# 데이터 크기 확인
if X_train.size == 0 or X_test.size == 0:
    raise ValueError("Loaded data is empty. Please check the data paths and files.")

# 데이터 정규화하기(0~1사이로)
X_train = X_train.astype("float") / 255
X_test  = X_test.astype("float")  / 255

y_train_one_hot = to_categorical(y_train, nb_classes)
y_test_one_hot = to_categorical(y_test, nb_classes)

print('X_train shape:', X_train.shape)
print('y_train shape:', y_train.shape)

# 모델 구조 정의 
model = Sequential()
model.add(Conv2D(32, (3, 3), input_shape=(35, 35, 3), padding='same'))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Conv2D(64, (3, 3), padding='same'))
model.add(Activation('relu'))

model.add(Conv2D(64, (3, 3)))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

# 전결합층
model.add(Flatten())    # 벡터형태로 reshape
model.add(Dense(512))   # 출력
model.add(Activation('relu'))
model.add(Dropout(0.5))

model.add(Dense(nb_classes))
model.add(Activation('softmax'))

# 모델 구축하기
model.compile(loss='categorical_crossentropy',   # 최적화 함수 지정
              optimizer='rmsprop',
              metrics=['accuracy'])

# 모델 저장 경로
model_file = os.path.abspath("./model/model2.h5")

if os.path.exists(model_file):
    # 기존에 저장된 모델 불러들이기
    model = load_model(model_file)
else:
    # 학습한 모델 저장
    model.fit(X_train, y_train_one_hot, batch_size=32, epochs=15)
    model.save(model_file)

# 모델 평가
score = model.evaluate(X_test, y_test_one_hot, verbose=0)
print('Test loss:', score[0])
print('Test accuracy:', score[1])


