<template>
    <div class="edit-post">
      <h1>Edit Post</h1>
      <img :src="`${store.API_URL}${post?.image}`" alt="Post Image" />
      <textarea v-model="content" rows="10" cols="30"></textarea>
      <button @click="updatePost">Update</button>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  import axios from 'axios'
  import { useCommunity } from '@/stores/community'
  import { useCounterStore } from '@/stores/counter'
  const tokenstore = useCounterStore()

  const route = useRoute()
  const router = useRouter()
  const store = useCommunity()
  
  const content = ref('')
  const post = ref('')
  const fetchPost = async () => {
    try {
      const response = await axios.get(`${store.API_URL}/articles/detail_post/${route.params.id}/`)
      console.log(response.data);
      content.value = response.data.content
      post.value = response.data[0]
    } catch (error) {
      console.error('Error fetching post:', error)
    }
  }
  
  const updatePost = async () => {
    try {
      await axios.put(`${store.API_URL}/articles/update_post/${route.params.id}/`, {
        content: content.value
      }, {
        headers: {
          'Authorization': `Token ${tokenstore.token}`
        }
      })
      router.push({ name: 'PostDetail', params: { id: route.params.id } })
    } catch (error) {
      console.error('Error updating post:', error)
    }
  }
  
  onMounted(fetchPost)
  </script>
  
  <style scoped>
  .edit-post {
    padding: 20px;
  }
  
  .edit-post textarea {
    width: 100%;
    margin-top: 10px;
  }
  
  .edit-post button {
    margin-top: 10px;
  }
  </style>
  