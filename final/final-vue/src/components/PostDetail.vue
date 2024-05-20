<template>
    <div class="post-detail">
      <h1>{{ userid }}번 Post</h1>
      <RouterLink :to="{ name: 'EditPost', params: { id: userid } }">Edit</RouterLink>
    </div>
  </template>
  
  <script setup>
  import { onMounted, ref } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  import axios from 'axios'
  import { useCounterStore } from '@/stores/counter'

  const route = useRoute()
  const store = useCounterStore()

  const userid = route.params.id

  const router = useRouter()
  const post = ref(null)

  
  const fetchPost = async () => {
    try {
      const response = await axios.get(`${store.API_URL}/get_post/${route.params.id}/`)
      post.value = response.data
    } catch (error) {
      console.error('Error fetching post:', error)
    }
  }
  

  
  const deletePost = async (postId) => {
    try {
      await axios.delete(`${store.API_URL}/delete_post/${postId}/`, {
        headers: {
          'Authorization': `Token ${store.token}`
        }
      })
      router.push({ name: 'Community' })
    } catch (error) {
      console.error('Error deleting post:', error)
    }
  }
  
  onMounted(fetchPost)
  </script>
  
  <style scoped>
  .post-detail {
    padding: 20px;
  }
  
  .post-detail img {
    max-width: 100%;
    margin-top: 10px;
  }
  
  .post-detail p {
    margin-top: 10px;
  }
  
  .post-detail button {
    margin-top: 10px;
  }
  </style>
  