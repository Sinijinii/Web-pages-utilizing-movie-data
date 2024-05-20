<!-- ProfileView.vue -->
<template>
    <div class="profile">
      <h1>My Profile</h1>
      <div class="feed">
        <div v-for="post in posts" :key="post.id" class="post">
          <img :src="post.image" alt="Post Image" />
          <p>{{ post.content }}</p>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import axios from 'axios'
  
  const posts = ref([])
  
  const fetchMyPosts = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/my_posts/')
      posts.value = response.data
    } catch (error) {
      console.error('Error fetching posts:', error)
    }
  }
  
  onMounted(fetchMyPosts)
  </script>
  
  <style scoped>
  .profile {
    max-width: 600px;
    margin: 0 auto;
  }
  
  .feed {
    margin-top: 20px;
  }
  
  .post {
    border: 1px solid #ccc;
    padding: 10px;
    margin-bottom: 20px;
  }
  </style>
  