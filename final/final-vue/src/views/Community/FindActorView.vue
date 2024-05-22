<template>
  <div class="container upload-image">
    <h1 class="text-center title-medium">Find Similar Actor</h1>
    <div v-if="!similarActor" class="d-flex justify-content-center align-items-center">
      <div class="me-2">
        <input type="file" class="form-control" @change="onFileChange" accept="image/*" />
      </div>
      <button class="btn btn-primary" @click="uploadImage" :disabled="!selectedFile">Upload</button>
    </div>

    <div v-if="similarActor" class="result text-center mt-4">
      <h2 class="text-success batang-regular">{{ similarActor }}</h2>
      <img :src="`${userstore.API_URL}/media/${actorImageUrl}`" alt="Similar Actor Image" v-if="actorImageUrl" class="img-fluid mt-2 mx-auto d-block" />
      <div class="mt-3">
        <button class="btn btn-success me-2" @click="ShareResult">Share</button>
        <button class="btn btn-secondary" @click="resetForm">다시하기</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { useCommunity } from '@/stores/community'
import { useCounterStore } from '@/stores/counter'

const store = useCommunity()
const router = useRouter()
const selectedFile = ref(null)
const similarActor = ref(null)
let actorImageUrl = ref(null)
const userstore = useCounterStore()

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

const ShareResult = () => {
  router.push({
    name: 'SharePost',
    params: {
      similarActor: similarActor.value,
      actorImageUrl: actorImageUrl.value,
    }
  })
}

const resetForm = () => {
  selectedFile.value = null
  similarActor.value = null
  actorImageUrl.value = null
}
</script>

<style scoped>
@import url('@/assets/fonts/fonts.css');

.upload-image {
  margin-top: 50px;
  background-color: #FAF7F5; /* 배경색 */
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.upload-image h1 {
  color: #333333; /* 텍스트 색상 */
  font-family: 'TitleMedium', sans-serif; /* 제목 폰트 */
}

.upload-image .form-control {
  background-color: #FFF6E5; /* 크림색 */
  border: 1px solid #FF7F47; /* 주황색 */
  color: #333333; /* 텍스트 색상 */
  width: auto; /* 넓이를 줄임 */
}

.upload-image .btn-primary {
  background-color: #FF7F47; /* 주황색 */
  border: none;
}

.upload-image .btn-primary:disabled {
  background-color: #FFB899; /* 주황색의 더 연한 톤 */
}

.result h2 {
  color: #4C6A58; /* 녹색 */
  font-family: 'BatangRegular', serif; /* 결과 텍스트 폰트 */
}

.result img {
  max-width: 200px;
  border: 2px solid #4C6A58; /* 녹색 */
  border-radius: 5px;
}

.result .btn-success {
  background-color: #4C6A58; /* 녹색 */
  border: none;
}

.result .btn-secondary {
  background-color: #333333; /* 어두운 회색 */
  border: none;
}
</style>
