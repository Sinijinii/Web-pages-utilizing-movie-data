<template>
    <div class="liked-posts">
      <div class="sidebar">
        <RouterLink :to="{ name: 'Community' }">Community</RouterLink>
        <RouterLink :to="{ name: 'UploadImage' }">New Post</RouterLink>
        <RouterLink :to="{ name: 'ProfileView' }">My Profile</RouterLink>
        <RouterLink :to="{ name: 'LikePostsView' }">Liked Posts</RouterLink>
        <RouterLink :to="{ name: 'FindActor' }">FindActor</RouterLink>
        <RouterLink :to="{ name: 'ImageGenerator' }">ImageGenerator</RouterLink>
      </div>
      <div class="posts-content">
        <h1>Liked Posts</h1>
        <div v-if="likedPosts && likedPosts.length">
          <div v-for="post in likedPosts" :key="post.id" class="post">
            <RouterLink :to="{ name: 'PostDetail', params: { id: post.id } }">
              <img :src="`${store.API_URL}${post.image}`" alt="Post Image" />
              <p>{{ post.content }}</p>
              <p>{{ post.created_at }}</p>
              <p>Likes: {{ post.likes.length }}</p>
            </RouterLink>
            <button class="likebtn" @click="toggleLike(post)">
              {{ post.likes.includes(store.userId) ? 'Unlike' : 'Like' }}
            </button>
          </div>
        </div>
        <p v-else>No liked posts available.</p>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onBeforeMount } from 'vue'
  import axios from 'axios'
  import { useCounterStore } from '@/stores/counter'
  import { useCommunity } from '@/stores/community'
  
  const likedPosts = ref([])
  const store = useCommunity()
  const tokenstore = useCounterStore()
  
  const fetchLikedPosts = async () => {
    axios({
      method: 'get',
      url: `${store.API_URL}/articles/user_liked_posts/`,
      headers: {
        Authorization: `Token ${tokenstore.token}`
      }
    })
    .then(response => {
      likedPosts.value = response.data.liked_posts
    })
    .catch(error => {
      console.log(error)
    })
  }
  

  const toggleLike = (post) => {
    axios({
      method: 'post',
      url: `${store.API_URL}/articles/like_post/${post.id}/`,
      headers: {
        'Authorization': `Token ${tokenstore.token}`
      }
    })
      .then(response => {
        const liked = response.data.liked
        if (liked) {
          post.likes.push(store.userId)
        } else {
          const index = post.likes.indexOf(store.userId)
          if (index > -1) {
            post.likes.splice(index, 1)
          }
        }
      })
      .catch(error => {
        console.error('좋아요 기능 실패했다', error)
      })
  }


  onBeforeMount(() => {
    fetchLikedPosts()
  })
  </script>
  
  <style scoped>
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
  
  .posts-content {
    margin-left: 220px; /* 사이드바 뒤의 공간 확보 */
    padding: 20px;
  }
  
  .post {
    border: 1px solid #ccc;
    padding: 10px;
    margin-bottom: 20px;
  }
  
  .post img {
    max-width: 200px;
    margin-top: 10px;
  }
  
  .post p {
    margin-top: 10px;
  }
  </style>
  