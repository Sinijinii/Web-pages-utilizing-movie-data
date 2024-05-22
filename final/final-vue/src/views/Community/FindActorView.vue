<template>
  <div class="findactor">
    <div class="sidebar">
      <RouterLink :to="{ name: 'Community' }" class="sidebar-link" :class="{ active: $route.name === 'Community' }">Community</RouterLink>
      <RouterLink :to="{ name: 'UploadImage' }" class="sidebar-link" :class="{ active: $route.name === 'UploadImage' }">New Post</RouterLink>
      <RouterLink :to="{ name: 'ProfileView' }" class="sidebar-link" :class="{ active: $route.name === 'ProfileView' }">My Profile</RouterLink>
      <RouterLink :to="{ name: 'LikePostsView' }" class="sidebar-link" :class="{ active: $route.name === 'LikePostsView' }">Liked Posts</RouterLink>
      <RouterLink :to="{ name: 'FindActor' }" class="sidebar-link" :class="{ active: $route.name === 'FindActor' }">Find Actor</RouterLink>
      <RouterLink :to="{ name: 'ImageGenerator' }" class="sidebar-link" :class="{ active: $route.name === 'ImageGenerator' }">Image Generator</RouterLink>
    </div>
    <div class="container-fluid page-background">
      <div class="container py-5">
        <h1 class="text-center title-medium mb-5">Find Similar Actor</h1>
        <div v-if="!similarActor" class="d-flex justify-content-center align-items-center upload-section mb-5">
          <div class="me-2">
            <input type="file" class="form-control" @change="onFileChange" accept="image/*" />
          </div>
          <button class="btn btn-primary" @click="uploadImage" :disabled="!selectedFile">Upload</button>
        </div>

        <div v-if="similarActor" class="result card mx-auto p-4">
          <h2 class="text-success batang-regular text-center">{{ similarActor }}</h2>
          <img :src="`${userstore.API_URL}/media/${actorImageUrl}`" alt="Similar Actor Image" v-if="actorImageUrl" class="result-image mt-2" />
          <div class="mt-3 text-center">
            <button class="btn btn-success me-2" @click="showModal">Share</button>
            <button class="btn btn-secondary" @click="resetForm">다시하기</button>
          </div>
        </div>

        <!-- 모달 -->
        <div class="modal fade" id="shareModal" tabindex="-1" aria-labelledby="shareModalLabel" aria-hidden="true">
          <div class="modal-dialog modal-dialog-centered"> <!-- 모달 가운데 정렬 클래스 추가 -->
            <div class="modal-content">
              <div class="modal-header">
                <h5 class="modal-title" id="shareModalLabel">Share Your Result</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
              </div>
              <div class="modal-body">
                <SharePost :actorImageUrl="actorImageUrl" :similarActor="similarActor" />
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onUnmounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useCommunity } from '@/stores/community'
import { useCounterStore } from '@/stores/counter'
import { Modal } from 'bootstrap'
import SharePost from '@/components/Community/ShareResult.vue'

const store = useCommunity()
const router = useRouter()
const selectedFile = ref(null)
const similarActor = ref(null)
let actorImageUrl = ref(null)
const userstore = useCounterStore()
let modalInstance = null

const onFileChange = (event) => {
  selectedFile.value = event.target.files[0]
}

const uploadImage = async () => {
  if (!selectedFile.value) return

  const formData = new FormData()
  formData.append('image', selectedFile.value)

  try {
    const response = await axios.post(`${store.API_URL}/articles/find_similar_actor/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    similarActor.value = response.data.similar_actor
    actorImageUrl.value = response.data.img_url
  } catch (error) {
    console.error('Error uploading image:', error)
  }
}

const showModal = () => {
  const modalElement = document.getElementById('shareModal')
  modalInstance = new Modal(modalElement)
  modalInstance.show()

  modalElement.addEventListener('hidden.bs.modal', resetForm)
}

onUnmounted(() => {
  if (modalInstance) {
    modalInstance.hide()
    document.body.classList.remove('modal-open')
    const modalBackdrop = document.querySelector('.modal-backdrop')
    if (modalBackdrop) {
      modalBackdrop.remove()
    }
  }
})

const resetForm = () => {
  selectedFile.value = null
  similarActor.value = null
  actorImageUrl.value = null
}

</script>

<style scoped>
@import url('@/assets/fonts/fonts.css');

.findactor {
  display: flex;
}
.sidebar {
  width: 200px;
  padding: 20px;
  background-color: #4C6A58; /* 짙은 녹색 배경 */
  min-height: 100vh; /* 화면 전체 높이 */
  position: fixed; /* 사이드바를 고정 */
  left: 0; /* 왼쪽 끝에 붙임 */
  top: 0; /* 상단 끝에 붙임 */
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

.page-background {
  background-color: #FAF7F5; /* 전체 페이지 배경색 */
  min-height: 100vh;
  flex-grow: 1;
}

.container {
  background-color: #FFF6E5; /* 크림색 배경 */
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-left: 220px; /* 사이드바의 너비와 여백 확보 */
  padding: 20px;
  width: calc(100% - 220px); /* 전체 너비에서 사이드바 너비를 뺌 */
}

.title-medium {
  color: #333333; /* 텍스트 색상 */
  font-family: 'TitleMedium', sans-serif; /* 제목 폰트 */
}

.upload-section {
  background-color: #FFF6E5; /* 크림색 배경 */
  border: 1px solid #4C6A58; /* 어두운 녹색 테두리 */
  padding: 20px;
  border-radius: 10px;
}

.upload-section .form-control {
  background-color: #FFF6E5; /* 크림색 */
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

.result {
  background-color: #FFF6E5; /* 크림색 배경 */
  border: 1px solid #4C6A58; /* 어두운 녹색 테두리 */
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  text-align: center; /* 결과 섹션 전체 텍스트 가운데 정렬 */
}

.result h2 {
  color: #4C6A58; /* 녹색 */
  font-family: 'BatangRegular', serif; /* 결과 텍스트 폰트 */
}

.result-image {
  max-width: 400px; /* 이미지 크기 조절 */
  border: 2px solid #4C6A58; /* 녹색 */
  border-radius: 5px;
  display: block;
  margin: 10px auto; /* 이미지 가운데 정렬 */
}

.result .btn-success {
  background-color: #4C6A58; /* 녹색 */
  border: none;
}

.result .btn-secondary {
  background-color: #333333; /* 어두운 회색 */
  border: none;
}

.modal-content {
  background-color: #FAF7F5; /* 모달 배경색 */
}

.modal-header,
.modal-footer {
  border: none;
}

.modal-dialog-centered {
  display: flex;
  align-items: center;
  min-height: calc(100% - 1rem); /* 화면 중앙에 더 가까이 위치 */
}
</style>
