<template>
  <div class="edit-post-page">
    <div class="edit-post-container">
      <h1 class="title">Edit Post</h1>
      <div class="image-container">
        <img :src="`${store.API_URL}${post?.image}`" alt="Post Image" class="post-image" />
      </div>
      <textarea v-model="content" rows="10" class="edit-textarea"></textarea>
      <button @click="updatePost" class="update-button">Update</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { useCommunity } from '@/stores/community'
import { useCounterStore } from '@/stores/counter'
const tokenstore = useCounterStore()

const route = useRoute()
const router = useRouter()
const store = useCommunity()

const content = ref('')
const post = ref('')

const fetchPost = async () => {
  try {
    const response = await axios.get(`${store.API_URL}/articles/detail_post/${route.params.id}/`)
    console.log(response.data)
    content.value = response.data.content
    post.value = response.data[0]
  } catch (error) {
    console.error('Error fetching post:', error)
  }
}

const updatePost = async () => {
  try {
    await axios.put(`${store.API_URL}/articles/update_post/${route.params.id}/`, {
      content: content.value
    }, {
      headers: {
        'Authorization': `Token ${tokenstore.token}`
      }
    })
    router.push({ name: 'PostDetail', params: { id: route.params.id } })
  } catch (error) {
    console.error('Error updating post:', error)
  }
}

onMounted(fetchPost)
</script>

<style scoped>
@import url('@/assets/fonts/fonts.css');

.edit-post-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f7f7f7;
  padding: 20px;
}

.edit-post-container {
  background-color: white;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 600px;
  text-align: center;
}

.title {
  color: #333;
  font-family: 'TitleMedium', sans-serif;
  margin-bottom: 20px;
}

.image-container {
  margin-bottom: 20px;
}

.post-image {
  width: 100%;
  height: auto;
  border-radius: 10px;
  object-fit: cover;
}

.edit-textarea {
  width: 100%;
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #ddd;
  font-family: 'Arial', sans-serif;
  resize: vertical;
}

.update-button {
  background-color: #4C6A58;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  font-family: 'TitleMedium', sans-serif;
  cursor: pointer;
  margin-top: 20px;
}

.update-button:hover {
  background-color: #3B5241;
}
</style>
