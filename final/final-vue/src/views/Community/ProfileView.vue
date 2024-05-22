<template>
  <div class="profile-page">
    <div class="sidebar">
      <RouterLink :to="{ name: 'Community' }" class="sidebar-link" :class="{ active: $route.name === 'Community' }">Community</RouterLink>
      <RouterLink :to="{ name: 'UploadImage' }" class="sidebar-link" :class="{ active: $route.name === 'UploadImage' }">New Post</RouterLink>
      <RouterLink :to="{ name: 'ProfileView' }" class="sidebar-link" :class="{ active: $route.name === 'ProfileView' }">My Profile</RouterLink>
      <RouterLink :to="{ name: 'LikePostsView' }" class="sidebar-link" :class="{ active: $route.name === 'LikePostsView' }">Liked Posts</RouterLink>
      <RouterLink :to="{ name: 'FindActor' }" class="sidebar-link" :class="{ active: $route.name === 'FindActor' }">Find Actor</RouterLink>
      <RouterLink :to="{ name: 'ImageGenerator' }" class="sidebar-link" :class="{ active: $route.name === 'ImageGenerator' }">Image Generator</RouterLink>
    </div>
    <div class="profile-content">
      <div class="profile-info">
        <img :src="`${store.API_URL}${profileImage}`" alt="User Profile Picture" class="profile-picture mb-3" />
        <h1 class="title-medium">{{ username }}</h1>
        <div class="profile-stats">
          <div>
            <p class="stat-number">{{ posts.length }}</p>
            <p class="stat-label">게시물</p>
          </div>
          <div>
            <p class="stat-number">{{ totalLikes }}</p>
            <p class="stat-label">좋아요</p>
          </div>
        </div>
        <div class="profile-actions mt-3">
          <button @click="toggleEditMode" class="btn btn-primary me-2">프로필 수정</button>
          <RouterLink :to="{ name: 'LikePostsView' }" class="btn btn-outline-primary">좋아요한 페이지</RouterLink>
        </div>
      </div>

      <div v-if="editMode" class="edit-profile-card">
        <input type="file" @change="onFileChange" class="form-control mb-3" />
        <button @click="uploadProfileImage" class="btn btn-success">새 프로필 사진 업로드</button>
        <button @click="toggleEditMode" class="btn btn-secondary mt-3">닫기</button>
      </div>

      <div class="my-posts">
        <h2 class="title-medium mb-4">My Posts</h2>
        <div v-if="posts && posts.length" class="posts-grid">
          <div v-for="post in posts" :key="post.id" class="post">
            <RouterLink :to="{ name: 'PostDetail', params: { id: post.id } }">
              <img :src="`${store.API_URL}${post.image}`" alt="Post Image" class="post-image" />
            </RouterLink>
          </div>
        </div>
        <p v-else>No posts available.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onBeforeMount } from 'vue'
import axios from 'axios'
import { useCounterStore } from '@/stores/counter'
import { useCommunity } from '@/stores/community'

const posts = ref([])
const profileImage = ref('')
const totalLikes = ref(0)
const username = ref('')
const selectedFile = ref(null)
const editMode = ref(false)

const store = useCommunity()
const tokenstore = useCounterStore()

const fetchMyPosts = async () => {
  axios({
    method: 'get',
    url: `${store.API_URL}/articles/user_profile/`,
    headers: {
      Authorization: `Token ${tokenstore.token}`
    }
  })
  .then(response => {
    posts.value = response.data.posts
    profileImage.value = response.data.profile_image
    username.value = response.data.username
    totalLikes.value = response.data.total_likes
  })
  .catch(error => {
    console.log(error)
  })
}

const onFileChange = (event) => {
  selectedFile.value = event.target.files[0]
}

const uploadProfileImage = () => {
  const formData = new FormData()
  formData.append('profile_image', selectedFile.value)

  axios({
    method: 'post',
    url: `${store.API_URL}/articles/upload_profile_image/`,
    headers: {
      Authorization: `Token ${tokenstore.token}`,
      'Content-Type': 'multipart/form-data'
    },
    data: formData
  })
  .then(response => {
    profileImage.value = response.data.profile_image
    toggleEditMode()
  })
  .catch(error => {
    console.log(error)
  })
}

const toggleEditMode = () => {
  editMode.value = !editMode.value
}

onBeforeMount(() => {
  fetchMyPosts()
})
</script>

<style scoped>
@import url('@/assets/fonts/fonts.css');

.profile-page {
  display: flex;
  justify-content: center; /* 페이지를 가운데 정렬 */
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

.profile-content {
  margin-left: 220px; /* 사이드바의 너비와 여백 확보 */
  padding: 20px;
  width: calc(100% - 220px); /* 전체 너비에서 사이드바 너비를 뺌 */
}

.profile-info {
  text-align: center;
  margin-bottom: 20px;
  border: 1px solid #ddd; /* 옅은 회색 테두리 */
  border-radius: 10px;
  padding: 20px;
}

.profile-picture {
  width: 150px; /* 프로필 사진 크기를 조금 더 크게 설정 */
  height: 150px;
  border-radius: 50%;
  object-fit: cover;
}

.profile-stats {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 10px;
}

.profile-stats div {
  text-align: center;
}

.stat-number {
  font-size: 1.2em;
  font-weight: bold;
}

.stat-label {
  font-size: 0.9em;
  color: #555;
}

.profile-actions {
  display: flex;
  justify-content: center;
  gap: 10px;
}

.edit-profile-card {
  border: 1px solid #ddd;
  padding: 20px;
  margin-bottom: 20px;
  text-align: center;
  background-color: #fff;
  border-radius: 10px;
}

.my-posts {
  margin-bottom: 20px;
}

.posts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); /* 이미지 크기를 키움 */
  gap: 20px; /* 이미지 사이에 여백 추가 */
}

.post img {
  width: 250px; /* 이미지의 너비와 높이 조정 */
  height: 180px;
  object-fit: cover;
  border-radius: 10px;
}

.btn-primary, .btn-outline-primary {
  background-color: #FF7F47; /* 주황색 */
  border: none;
}

.btn-outline-primary {
  background-color: transparent;
  color: #FF7F47;
  border: 1px solid #FF7F47;
}

.btn-primary:hover, .btn-outline-primary:hover {
  background-color: #FFB899; /* 주황색의 더 연한 톤 */
}
</style>
