<template>
    <div class="post-detail">
      <h1>{{ userid }}번 Post</h1>

      <RouterLink :to="{ name: 'EditPost', params: { id: userid } }">Edit</RouterLink>

      <p>Likes: {{ post.likes.length }}</p>
<!-- 
      <button @click="toggleLike(post)">
        {{ post.likes.some(like => like.id === store.user.id) ? 'Unlike' : 'Like' }}
      </button> -->
      
    </div>
</template>
  
<script setup>
  import { onMounted, ref } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  import axios from 'axios'
  import { useCounterStore } from '@/stores/counter'

  const route = useRoute()
  const store = useCounterStore()

  const userid = route.params.id

  const router = useRouter()
  const post = ref(null)
  
  const fetchPost = async () => {
    try {
      const response = await axios.get(`${store.API_URL}/get_post/${route.params.id}/`)
      post.value = response.data
    } catch (error) {
      console.error('Error fetching post:', error)
    }
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
  

  // const toggleLike = async (post) => {
  //   try {
  //     const response = await axios.post(`${store.API_URL}/like_post/${post.id}/`, {}, {
  //       post_id: post.id
  //     }, {
  //       headers: {
  //         'Authorization': `Token ${store.token}`
  //       }
  //     })
  //     if (response.data.liked) {
  //       post.likes.push({ id: store.user.id })
  //     } else {
  //       post.likes = post.likes.filter(user => user.id !== store.user.id)
  //     }
  //   } catch (error) {
  //     console.error('좋아요 기능 실패했다', error)
  //   }
  // }

  onMounted(fetchPost)
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
  