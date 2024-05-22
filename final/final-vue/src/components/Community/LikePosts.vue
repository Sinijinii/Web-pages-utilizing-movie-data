<template>
  <div class="liked-posts-page">
    <div class="sidebar">
      <RouterLink :to="{ name: 'Community' }" class="sidebar-link" :class="{ active: $route.name === 'Community' }">Community</RouterLink>
      <RouterLink :to="{ name: 'UploadImage' }" class="sidebar-link" :class="{ active: $route.name === 'UploadImage' }">New Post</RouterLink>
      <RouterLink :to="{ name: 'ProfileView' }" class="sidebar-link" :class="{ active: $route.name === 'ProfileView' }">My Profile</RouterLink>
      <RouterLink :to="{ name: 'LikePostsView' }" class="sidebar-link" :class="{ active: $route.name === 'LikePostsView' }">Liked Posts</RouterLink>
      <RouterLink :to="{ name: 'FindActor' }" class="sidebar-link" :class="{ active: $route.name === 'FindActor' }">Find Actor</RouterLink>
      <RouterLink :to="{ name: 'ImageGenerator' }" class="sidebar-link" :class="{ active: $route.name === 'ImageGenerator' }">Image Generator</RouterLink>
    </div>
    <div class="posts-content">
      <h1 class="title-medium">Liked Posts</h1>
      <div v-if="likedPosts && likedPosts.length" class="posts-grid">
        <div v-for="post in likedPosts" :key="post.id" class="post">
          <RouterLink :to="{ name: 'PostDetail', params: { id: post.id } }">
            <img :src="`${store.API_URL}${post.image}`" alt="Post Image" class="post-image" />
          </RouterLink>
          <p>{{ post.content }}</p>
          <p>{{ post.created_at }}</p>
          <p>Likes: {{ post.likes.length }}</p>
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
@import url('@/assets/fonts/fonts.css');

.liked-posts-page {
  display: flex;
}

.sidebar {
  width: 200px;
  padding: 20px;
  background-color: #4C6A58; /* 짙은 녹색 배경 */
  min-height: 100vh; /* 화면 전체 높이 */
  position: fixed; /* 사이드바를 고정 */
  left: 0; /* 왼쪽 끝에 붙임 */
  top: 0; /* 상단 끝에 붙임 */
}

.sidebar-link {
  display: block;
  color: #FFF6E5; /* 크림색 텍스트 */
  font-family: 'TitleMedium', sans-serif; /* 제목 폰트 */
  text-decoration: none;
  padding: 10px 15px;
  margin-bottom: 10px;
  border-radius: 5px;
  transition: background-color 0.3s;
}

.sidebar-link.active {
  background-color: #FF7F47; /* 활성 링크의 배경색 */
  color: #FFF; /* 활성 링크의 텍스트 색상 */
}

.sidebar-link:hover {
  background-color: #333333; /* 어두운 회색 배경 */
}

.posts-content {
  margin-left: 220px; /* 사이드바의 너비와 여백 확보 */
  padding: 20px;
  width: calc(100% - 220px); /* 전체 너비에서 사이드바 너비를 뺌 */
}

.title-medium {
  color: #333333; /* 텍스트 색상 */
  font-family: 'TitleMedium', sans-serif; /* 제목 폰트 */
  text-align: center;
  margin-bottom: 20px;
}

.posts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); /* 이미지 크기를 키움 */
  gap: 20px; /* 이미지 사이에 여백 추가 */
}

.post {
  background-color: #FAF7F5; /* 하얀색 배경 */
  border: 1px solid #ddd; /* 옅은 회색 테두리 */
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 20px;
  text-align: center;
}

.post img {
  width: 250px; /* 이미지의 너비와 높이 조정 */
  height: 180px;
  object-fit: cover;
  border-radius: 10px;
  margin-bottom: 10px;
}

.likebtn {
  background-color: #FF7F47;
  border: none;
  padding: 5px 10px;
  cursor: pointer;
  border-radius: 5px;
  font-family: 'TitleMedium', sans-serif;
  color: white;
}

.likebtn:hover {
  background-color: #FFB899; /* 주황색의 더 연한 톤 */
}
</style>
