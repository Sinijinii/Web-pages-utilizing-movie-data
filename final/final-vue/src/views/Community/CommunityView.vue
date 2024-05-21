<template>
  <div class="community">
    <div class="sidebar">
      <RouterLink :to="{ name: 'Community' }">Community</RouterLink>
      <RouterLink :to="{ name: 'UploadImage' }">New Post</RouterLink>
      <RouterLink :to="{ name: 'ProfileView' }">My Profile</RouterLink>
      <RouterLink :to="{ name: 'FollowingView' }">Following</RouterLink>
      <RouterLink :to="{ name: 'FindActor' }">FindActor</RouterLink>
      <RouterLink :to="{ name: 'ImageGenerator' }">ImageGenerator</RouterLink>
    </div>
    <div class="posts">
      <h1>Community Posts</h1>
      <div v-if="posts && posts.length">
        <div v-for="post in posts" :key="post.id" class="post">
          <RouterLink v-if="post.id" :to="{ name: 'PostDetail', params: { id: post.id } }">View Details</RouterLink>
          <img :src="`${store.API_URL}${post.image}`" alt="Post Image" />
          <p>{{ post.content }}</p>
          <p>{{ post.created_at }}</p>
          <p>Likes: {{ post.likes.length }}</p>
          <p>{{ post.user.username }}</p>
          <div v-if="userstore.LoginUsername === post.user.username">
            <RouterLink :to="{ name: 'EditPost', params: { id: post.id } }">Edit</RouterLink>
            <button @click="deletePost(post.id)">Delete</button>
          </div>
        </div>
      </div>
      <p v-else>No posts available.</p>
    </div>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import { onMounted, ref } from 'vue'
import axios from 'axios'
import { useCommunity } from '@/stores/community'
import { useCounterStore } from '@/stores/counter'

const userstore = useCounterStore()
const posts = ref([])

const store = useCommunity()

const fetchPosts = async () => {
  axios({
    method:'get',
    url:`${store.API_URL}/articles/get_posts/`
  })
  .then((response)=>{
    posts.value = response.data
  })
  .catch((error) => {
        console.log(error)
  })
}

const deletePost = async (postId) => {
  axios({
    method:'delete',
    url: `${store.API_URL}/articles/delete_post/${postId}/`,
    headers: {
        'Authorization': `Token ${store.token}`
      }
  })
  .then((response)=>{
    posts.value = posts.value.filter(post => post.id !== postId)
  })
  .catch((error) => {
        console.log(error)
  })
}

onMounted(() => {
  fetchPosts()
})
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
