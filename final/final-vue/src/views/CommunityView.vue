<template>
  <div class="community">
    <h1>Community</h1>
    <div class="feed">
      <div v-for="post in posts" :key="post.id" class="post">
        <img :src="post.image" alt="Post Image" />
        <p>{{ post.content }}</p>
        <button @click="likePost(post.id)">Like</button>
        <button @click="followUser(post.user.id)">Follow</button>
        <div class="comments">
          <p v-for="comment in post.comments" :key="comment.id">{{ comment.text }}</p>
          <input v-model="newComment" placeholder="Add a comment" />
          <button @click="addComment(post.id)">Comment</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const posts = ref([])
const newComment = ref('')

const fetchPosts = async () => {
  try {
    const response = await axios.get('http://localhost:8000/articles/posts/')
    posts.value = response.data
  } catch (error) {
    console.error('Error fetching posts:', error)
  }
}

const likePost = async (postId) => {
  try {
    await axios.post(`http://localhost:8000/articles/posts/${postId}/like/`)
    fetchPosts()
  } catch (error) {
    console.error('Error liking post:', error)
  }
}

const followUser = async (userId) => {
  try {
    await axios.post(`http://localhost:8000/articles/users/${userId}/follow/`)
  } catch (error) {
    console.error('Error following user:', error)
  }
}

const addComment = async (postId) => {
  try {
    await axios.post(`http://localhost:8000/articles/posts/${postId}/comments/`, { text: newComment.value })
    newComment.value = ''
    fetchPosts()
  } catch (error) {
    console.error('Error adding comment:', error)
  }
}

onMounted(fetchPosts)
</script>

<style scoped>
.community {
  max-width: 600px;
  margin: 0 auto;
}

.feed {
  margin-top: 20px;
}

</style>