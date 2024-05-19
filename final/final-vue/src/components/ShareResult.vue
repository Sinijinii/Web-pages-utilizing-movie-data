<template>
  <div class="share-post">
    <h1>Share Your Result</h1>
    <img :src="actorImageUrl" alt="Similar Actor Image" /> <br>
    {{ similarActor }} <br>
    <textarea v-model="content" placeholder="Write something..."></textarea>
    <button @click="sharePost">Share</button>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import { useCounterStore } from '@/stores/counter'

const route = useRoute()
const fileStore = useCounterStore()

const actorImageUrl = route.params.actorImageUrl
const similarActor = route.params.similarActor

const content = ref('')

const sharePost = async () => {
  console.log(similarActor)
  console.log(content.value);
  
  await fileStore.sharePost(similarActor, content.value, actorImageUrl)
}
</script>

<style scoped>
.share-post {
  text-align: center;
  margin-top: 50px;
}

.share-post img {
  max-width: 200px;
  margin-top: 10px;
}

.share-post textarea {
  width: 80%;
  height: 100px;
  margin-top: 10px;
}

.share-post button {
  margin-top: 10px;
}
</style>
