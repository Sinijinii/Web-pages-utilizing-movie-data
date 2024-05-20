<template>
  <div class="following">
    <h1>Following</h1>
    <div v-for="post in followingPosts" :key="post.id" class="post">
      <h2>{{ post.user }}</h2>
      <img :src="post.image_url" alt="Post Image" />
      <p>{{ post.content }}</p>
      <p>{{ post.created_at }}</p>
      <p>Likes: {{ post.likes }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useCounterStore } from '@/stores/counter'

const store = useCounterStore()
const followingPosts = ref([])

onMounted(async () => {
  await store.getPosts()
  // 팔로우한 사람들의 게시글만 필터링
  followingPosts.value = store.posts.filter(post => {
    // 팔로우한 사용자 ID와 일치하는 게시글 필터링 로직 추가
    return true // 임시로 모든 게시글을 반환
  })
})
</script>

<style scoped>
.following {
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
