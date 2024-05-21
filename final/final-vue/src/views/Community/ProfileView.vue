<!-- ProfileView.vue -->
<template>
  <div class="profile">
    <div class="sidebar">
      <RouterLink :to="{ name: 'Community' }">Community</RouterLink>
      <RouterLink :to="{name: 'UploadImage'}">New Post</RouterLink>
      <RouterLink :to="{name: 'ProfileView'}">My Profile</RouterLink>
      <RouterLink :to="{name: 'FollowingView'}">Following</RouterLink>
      <RouterLink :to="{name: 'FindActor'}">FindActor</RouterLink>
      <RouterLink :to="{name:'ImageGenerator'}">ImageGenerator</RouterLink>
    </div>
    <div class="posts">
      <h1>My Profile</h1>
      <div v-for="post in posts" :key="post.id" class="post">
        <h2>{{ post.user.username }}</h2>
        <img :src="`${store.API_URL}${post.image}`" alt="Post Image" />
        <p>{{ post.content }}</p>
        <p>{{ post.created_at }}</p>
        <p>Likes: {{ post.likes.length }}</p>
      </div>
    </div>
  </div>
</template>
  
<script setup>
  import { onMounted, ref, onBeforeMount } from 'vue'
  import axios from 'axios'
  import { useCounterStore } from '@/stores/counter'
  import { useCommunity } from '@/stores/community'

  const posts = ref([])
  const store = useCommunity()
  const tokenstore = useCounterStore()
  const fetchMyPosts = async () => {
    axios({
      method:'get',
      url:`${store.API_URL}/articles/my_posts/`,
      headers: {
        Authorization: `Token ${tokenstore.token}`
      }
    })
    .then(response => {
      posts.value = response.data
      console.log(posts);
    })
    .catch(error => {
      console.log(error)
    })
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
  
  .feed {
    margin-top: 20px;
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
    width: 80%;
    margin-top: 10px;
  }
</style>
  