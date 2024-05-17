<template>
    <div class="share-post">
      <h1>Share Your Result</h1>
      <img :src="actorImageUrl" alt="Similar Actor Image" />
      <textarea v-model="content" placeholder="Write something..."></textarea>
      <button @click="sharePost">Share</button>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import axios from 'axios'
  import { useRoute, useRouter } from 'vue-router'
  
  // Props를 사용하여 router로부터 데이터를 받음
  const route = useRoute()
  const router = useRouter()
  const similarActor = route.params.similarActor
  const actorImageUrl = route.params.actorImageUrl
  const selectedFile = route.params.selectedFile // router로부터 받은 selectedFile

  // 값이 왜 없을까..
  console.log('adlfkjasdlkfjalksdfaAD');
  console.log(route.params);

  
  const content = ref('')
  
  const sharePost = async () => {
    if (!content.value) {
      alert('Please write something before sharing.')
      return
    }
  
    if (!selectedFile) { // selectedFile을 올바르게 체크
      alert('No file selected.')
      return
    }
  
    const formData = new FormData()
    formData.append('title', `Prediction result: ${similarActor}`)
    formData.append('content', content.value)
    formData.append('image', selectedFile) // 수정된 부분
  
    try {
      await axios.post('http://localhost:8000/upload_post/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
      alert('Result shared successfully!')
      router.push('/community')
    } catch (error) {
      console.error('Error sharing post:', error)
    }
  }
  </script>
  
  <style scoped>
  .share-post {
    text-align: center;
    margin-top: 50px;
  }
  
  .share-post img {
    max-width: 200px;
    margin-top: 10px;
  }
  
  .share-post textarea {
    width: 80%;
    height: 100px;
    margin-top: 10px;
  }
  
  .share-post button {
    margin-top: 10px;
  }
  </style>
  