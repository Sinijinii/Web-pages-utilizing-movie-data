<template>
  <div class="profile">
    <div class="sidebar">
      <RouterLink :to="{ name: 'Community' }">Community</RouterLink>
      <RouterLink :to="{ name: 'UploadImage' }">New Post</RouterLink>
      <RouterLink :to="{ name: 'ProfileView' }">My Profile</RouterLink>
      <RouterLink :to="{ name: 'LikePostsView' }">Liked Posts</RouterLink>
      <RouterLink :to="{ name: 'FindActor' }">Find Actor</RouterLink>
      <RouterLink :to="{ name: 'ImageGenerator' }">Image Generator</RouterLink>
    </div>
    <div class="profile-content">
      <div class="profile-info">
        <img :src="profileImage" alt="User Profile Picture" class="profile-picture" />
        <h1>{{ username }}</h1>
        <p>Total Likes: {{ totalLikes }}</p>
        <button @click="toggleEditMode">Edit Profile</button>
      </div>

      <div v-if="editMode" class="edit-profile-card">
        <input type="file" @change="onFileChange" />
        <button @click="uploadProfileImage">Upload New Profile Picture</button>
        <button @click="toggleEditMode">Close</button>
      </div>

      <div class="liked-posts-link">
        <RouterLink :to="{ name: 'LikePostsView' }">See Liked Posts</RouterLink>
      </div>

      <div class="my-posts">
        <h2>My Posts</h2>
        <div v-if="posts && posts.length">
          <div v-for="post in posts" :key="post.id" class="post">
            <RouterLink :to="{ name: 'PostDetail', params: { id: post.id } }">
              <img :src="`${store.API_URL}${post.image}`" alt="Post Image" />
              <p>{{ post.content }}</p>
              <p>{{ post.created_at }}</p>
              <p>Likes: {{ post.likes.length }}</p>
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

.profile {
  display: flex;
}

.profile-content {
  margin-left: 220px; /* 사이드바 뒤의 공간 확보 */
}

.profile-info {
  text-align: center;
  margin-bottom: 20px;
}

.profile-picture {
  width: 100px;
  height: 100px;
  border-radius: 50%;
}

.edit-profile-card {
  border: 1px solid #ccc;
  padding: 20px;
  margin-bottom: 20px;
  text-align: center;
}

.liked-posts-link {
  margin-bottom: 20px;
}

.posts, .liked-posts, .my-posts {
  margin-bottom: 20px;
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
