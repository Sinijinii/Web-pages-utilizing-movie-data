<template>
  <div class="community">
    <div class="sidebar">
      <router-link to="/upload">New Post</router-link>
      <router-link to="/profile">My Profile</router-link>
      <router-link to="/following">Following</router-link>
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
import { onMounted, ref } from 'vue'
import axios from 'axios'

const posts = ref([])

const fetchPosts = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/articles/get_posts/')
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
