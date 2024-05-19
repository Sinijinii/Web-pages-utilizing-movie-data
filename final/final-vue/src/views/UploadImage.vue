<template>
    <div class="upload-image">
      <h1>New Post</h1>
      <input type="file" @change="onFileChange" accept="image/*" />
      <textarea v-model="content" placeholder="Write something..."></textarea>
      <button @click="uploadImage" :disabled="!selectedFile">Upload</button>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import { useRouter } from 'vue-router'
  import { useCounterStore } from '@/stores/counter'
  import axios from 'axios'
  
  const fileStore = useCounterStore()
  const router = useRouter()
  
  const selectedFile = ref(null)
  const content = ref('')
  
  const onFileChange = (event) => {
    selectedFile.value = event.target.files[0]
    fileStore.setFile(selectedFile.value)
  }
  
  const uploadImage = async () => {
    if (!selectedFile.value) return
  
    const formData = new FormData()
    formData.append('image', selectedFile.value)
  
    try {
      const response = await axios.post('http://localhost:8000/articles/find_similar_actor/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
      const actorImageUrl = response.data.img_url
  
      fileStore.similarActor = response.data.similar_actor
      fileStore.actorImageUrl = actorImageUrl
  
      await fileStore.sharePost(content.value, actorImageUrl)
      router.push('/community')
    } catch (error) {
      console.error('Error uploading image:', error)
    }
  }
  </script>
  
  <style scoped>
  .upload-image {
    text-align: center;
    margin-top: 50px;
  }
  
  .upload-image textarea {
    width: 80%;
    height: 100px;
    margin-top: 10px;
  }
  
  .upload-image button {
    margin-top: 10px;
  }
  </style>
  