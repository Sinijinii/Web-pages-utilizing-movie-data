<template>
    <div class="post-detail">
      <h1>{{ postid }}번 Post</h1>
      <img :src="`${store.API_URL}${post?.image}`" alt="Post Image" />
        <p>{{ post?.content }}</p>
        <p>{{ post?.created_at }}</p>
      <div v-if="userstore.LoginUsername === post?.user.username">
        <RouterLink :to="{ name: 'EditPost', params: { id: postId } }">Edit</RouterLink>
        <button @click="deletePost(postId)">Delete</button>
      </div>

    </div>
  </template>
  
  <script setup>
  import { onMounted, ref, onBeforeMount } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  import axios from 'axios'
  import { useCounterStore } from '@/stores/counter'
  import { useCommunity } from '@/stores/community'

  const route = useRoute()
  const store = useCommunity()
  const userstore = useCounterStore()
  const postid = route.params.id

  const router = useRouter()

  const post = ref(null)

  
  const fetchPost = async () => {
    axios({
      method:'get',
      url:`${store.API_URL}/articles/detail_post/${postid}/`,
    })
    .then(response => {
      post.value = response.data[0]
    })
    .catch(error => {
      console.log(error)
    })
  }
  

  
  const deletePost = async (postId) => {
    try {
      await axios.delete(`${store.API_URL}/delete_post/${postId}/`, {
        headers: {
          'Authorization': `Token ${store.token}`
        }
      })
      router.push({ name: 'Community' })
    } catch (error) {
      console.error('Error deleting post:', error)
    }
  }
  
  onBeforeMount(() => {
    fetchPost()
  })

  </script>
  

  <style scoped>
  .post-detail {
    padding: 20px;
  }
  
  .post-detail img {
    max-width: 100%;
    margin-top: 10px;
  }
  
  .post-detail p {
    margin-top: 10px;
  }
  
  .post-detail button {
    margin-top: 10px;
  }
  </style>
  