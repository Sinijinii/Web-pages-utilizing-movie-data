<template>
  <div class="community">
    <div class="sidebar">
      <RouterLink :to="{ name: 'Community' }">Community</RouterLink>
      <RouterLink :to="{name: 'UploadImage'}">New Post</RouterLink>
      <RouterLink :to="{name: 'ProfileView'}">My Profile</RouterLink>
      <RouterLink :to="{name: 'FollowingView'}">Following</RouterLink>
      <RouterLink :to="{name: 'FindActor'}">FindActor</RouterLink>
      <RouterLink :to="{name:'ImageGenerator'}">ImageGenerator</RouterLink>
    </div>
    <div class="posts">
      <h1>Community Posts</h1>
      <div v-for="post in posts" :key="post.id" class="post">
        <h2>{{ post.user.username }}</h2>
        <img :src="post.image" alt="Post Image" />
        <p>{{ post.content }}</p>
        <p>{{ post.created_at }}</p>
        <p>Likes: {{ post.likes.length }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { onMounted, ref } from 'vue'
import axios from 'axios'
import router from '@/router';
import { useCounterStore } from '@/stores/counter'

const posts = ref([])

const store = useCounterStore()
const fetchPosts = async () => {
  try {
    const response = await axios.get(`${store.API_URL}/articles/get_posts/`)
    posts.value = response.data
  } catch (error) {
    console.error('Error fetching posts:', error)
  }
}

onMounted(fetchPosts)
</script>

<style scoped>
.community {
  display: flex;
}

.sidebar {
  width: 200px;
  padding: 20px;
  background-color: #f0f0f0;
}

.sidebar a {
  display: block;
  margin-bottom: 10px;
  text-decoration: none;
  color: #000;
}

.posts {
  flex-grow: 1;
  padding: 20px;
}

.post {
  margin-bottom: 20px;
}

.post img {
  max-width: 200px;
  margin-top: 10px;
}

.post p {
  width: 80%;
  margin-top: 10px;
}
</style>
