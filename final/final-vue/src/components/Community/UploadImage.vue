<template>
  <div class="upload-page">
    <div class="sidebar">
      <RouterLink :to="{ name: 'MainView' }" class="sidebar-link" :class="{ active: $route.name === 'Mainpage' }">Mainpage</RouterLink>
      <hr>
      <RouterLink :to="{ name: 'Community' }" class="sidebar-link" :class="{ active: $route.name === 'Community' }">Community</RouterLink>
      <RouterLink :to="{ name: 'UploadImage' }" class="sidebar-link" :class="{ active: $route.name === 'UploadImage' }">New Post</RouterLink>
      <RouterLink :to="{ name: 'ProfileView', params: { username: userstore.LoginUsername } }" class="sidebar-link" :class="{ active: $route.name === 'ProfileView' }">My Profile</RouterLink>      <RouterLink :to="{ name: 'LikePostsView' }" class="sidebar-link" :class="{ active: $route.name === 'LikePostsView' }">Liked Posts</RouterLink>
      <RouterLink :to="{ name: 'FindActor' }" class="sidebar-link" :class="{ active: $route.name === 'FindActor' }">닮은꼴 배우찾기</RouterLink>
      <RouterLink :to="{ name: 'ImageGenerator' }" class="sidebar-link" :class="{ active: $route.name === 'ImageGenerator' }">나만의 영화 포스터</RouterLink>
    </div>
    <div class="upload page-background">
      <div class="container py-5">
        <!-- 이미지 선택 페이지 -->
        <h1 class="text-center title-medium mb-5">New Post</h1>
        <div v-if="step === 0" class="d-flex justify-content-center align-items-center upload-section mb-5">
          <div class="me-2">
            <input type="file" class="form-control" @change="onFileChange" accept="image/*" />
          </div>
          <button class="btn btn-primary" @click="nextStep" :disabled="!selectedFile">Next</button>
        </div>

        <!-- 글 작성 페이지 -->
        <div v-if="step === 1" class="write-section card mx-auto p-4">
          <div class="upload-image mb-3" :style="`background-image:url(${imageURL})`"></div>
          <div class="write">
            <textarea v-model="content" class="write-box" placeholder="Write something..."></textarea>
          </div>
          <div class="mt-3 text-center">
            <button class="btn btn-success me-2" @click="sharePost">Share</button>
            <button class="btn btn-secondary" @click="resetForm">다시하기</button>
          </div>
        </div>

        <!-- 업로드 완료 페이지 -->
        <div v-if="step === 2" class="completion-section text-center">
          <p>Post shared successfully!</p>
          <router-link to="/community" class="btn btn-secondary mt-3">Go to Community</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useCommunity } from '@/stores/community'
import { useCounterStore } from '@/stores/counter';

const userstore = useCounterStore()
const store = useCommunity()

const step = ref(0)
const selectedFile = ref(null)
const imageURL = ref("")
const content = ref("")

const onFileChange = (event) => {
  const file = event.target.files[0]
  if (file) {
    selectedFile.value = file
    imageURL.value = URL.createObjectURL(file)
    store.setFile(file)
  }
}

const nextStep = () => {
  step.value++
}

const sharePost = async () => {
  await store.uploadPost(content.value)
  step.value = 2
}

const resetForm = () => {
  step.value = 0
  selectedFile.value = null
  imageURL.value = ""
  content.value = ""
}
</script>

<style scoped>
@import url('@/assets/fonts/fonts.css');

.upload-page {
  display: flex;
  background-color:#FAF7F5;
}

.sidebar {
  width: 200px;
  padding: 20px;
  background-color: #4C6A58; /* 짙은 녹색 배경 */
  min-height: 100vh; /* 화면 전체 높이 */
}

.sidebar-link {
  display: block;
  color: #FFF6E5; /* 크림색 텍스트 */
  font-family: 'TitleMedium', sans-serif; /* 제목 폰트 */
  text-decoration: none;
  padding: 10px 15px;
  margin-bottom: 10px;
  border-radius: 5px;
  transition: background-color 0.3s;
}

.sidebar-link.active {
  background-color: #FF7F47; /* 활성 링크의 배경색 */
  color: #FFF; /* 활성 링크의 텍스트 색상 */
}

.sidebar-link:hover {
  background-color: #333333; /* 어두운 회색 배경 */
}

.upload {
  background-color: #FFF6E5; /* 전체 페이지 배경색 */
  min-height: 100vh;
  flex-grow: 1;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding-top: 20px;
}

.container {
  background-color: #FAF7F5; /* 크림색 배경 */
  margin: 10px 10px 10px 10px;
  padding: 20px;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.upload-section {
  background-color: #FAF7F5; /* 크림색 배경 */
  border: 1px solid #4C6A58; /* 어두운 녹색 테두리 */
  padding: 20px;
  border-radius: 10px;
  width: 100%;
  max-width: 500px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.upload-section .form-control {
  background-color: #FAF7F5; /* 크림색 */
  border: 1px solid #FF7F47; /* 주황색 */
  color: #333333; /* 텍스트 색상 */
}

.upload-section .btn-primary {
  background-color: #FF7F47; /* 주황색 */
  border: none;
}

.upload-section .btn-primary:disabled {
  background-color: #FFB899; /* 주황색의 더 연한 톤 */
}

.write-section {
  background-color: #FFF6E5; /* 크림색 배경 */
  border: 1px solid #4C6A58; /* 어두운 녹색 테두리 */
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  text-align: center; /* 섹션 전체 텍스트 가운데 정렬 */
  width: 100%;
  max-width: 600px;
}
.title-medium {
  color: #333333; /* 텍스트 색상 */
  font-family: 'TitleMedium', sans-serif; /* 제목 폰트 */
}
.upload-image {
  width: 100%;
  height: 450px;
  background-size: contain; /* 이미지 크기를 조절하여 원본 비율 유지 */
  background-repeat: no-repeat; /* 배경 이미지 반복 없음 */
  background-position: center;
  margin-bottom: 20px;
}

.write-box {
  border: 1px solid #4C6A58; /* 테두리 색상 */
  width: 90%;
  height: 100px;
  padding: 15px;
  margin: auto;
  display: block;
  outline: none;
  font-family: 'TitleMedium', sans-serif; /* 제목 폰트 */
  background-color: #FFF6E5; /* 크림색 배경 */
}

button.btn-primary {
  background-color: #FF7F47; /* 주황색 */
  border: none;
}

button.btn-primary:disabled {
  background-color: #FFB899; /* 주황색의 더 연한 톤 */
}

button.btn-success {
  background-color: #4C6A58; /* 녹색 */
  border: none;
}

button.btn-secondary {
  background-color: #333333; /* 어두운 회색 */
  border: none;
}

.completion-section {
  background-color: #FFF6E5; /* 크림색 배경 */
  border: 1px solid #4C6A58; /* 어두운 녹색 테두리 */
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  text-align: center; /* 섹션 전체 텍스트 가운데 정렬 */
  padding: 20px;
  margin-top: 20px; /* 위쪽 여백 추가 */
}
</style>
