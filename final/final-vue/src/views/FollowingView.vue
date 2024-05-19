<template>
    <div class="following">
      <h1>Following</h1>
      <div v-for="post in followingPosts" :key="post.id" class="post">
        <h2>{{ post.user }}</h2>
        <img :src="post.image_url" alt="Post Image" />
        <p>{{ post.content }}</p>
        <p>{{ post.created_at }}</p>
        <p>Likes: {{ post.likes }}</p>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { useCounterStore } from '@/stores/counter'
  
  const fileStore = useCounterStore()
  const followingPosts = ref([])

  </script>
  
  <style scoped>

  </style>