<template>
  <div class="card share-post">
    <div class="card-body">
      <img :src="`${userstore.API_URL}/media/${actorImageUrl}`" class="card-img-top" alt="Similar Actor Image" /> <br>
      <p class="card-text">{{ similarActor }}</p>
      <textarea v-model="content" class="form-control" placeholder="Write something..."></textarea>
      <div class="d-flex justify-content-center">
        <button @click="sharePost" class="btn btn-primary mt-3">Share</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useCommunity } from '@/stores/community'
import { useCounterStore } from '@/stores/counter'

const props = defineProps({
  actorImageUrl: String,
  similarActor: String
})

const store = useCommunity()
const userstore = useCounterStore()

const content = ref('')

const sharePost = () => {
  store.uploadResult(content.value, props.actorImageUrl)
  console.log('여기는 ShareResult.vue');
  console.log(props.actorImageUrl);
}
</script>

<style scoped>
@import url('@/assets/fonts/fonts.css');

body {
  background-color: #FAF7F5; /* 전체 페이지 배경색 */
}

.share-post {
  max-width: 500px;
  margin: 0 auto;
  margin-top: 50px;
  background-color: #FAF7F5; /* 배경색 */
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.card-title {
  color: #333333; /* 텍스트 색상 */
  font-family: 'TitleMedium', sans-serif; /* 제목 폰트 */
}

.card-text {
  color: #4C6A58; /* 녹색 */
  font-family: 'BatangRegular', serif; /* 텍스트 폰트 */
}

.card-img-top {
  max-width: 100%;
  margin-top: 10px;
  border: 2px solid #4C6A58; /* 녹색 */
  border-radius: 5px;
}

.form-control {
  margin-top: 10px;
  background-color: #FFF6E5; /* 크림색 */
  border: 1px solid #FF7F47; /* 주황색 */
  border-radius: 5px;
  color: #333333; /* 텍스트 색상 */
  font-family: 'BatangRegular', serif; /* 텍스트 폰트 */
  padding: 10px;
}

.btn-primary {
  background-color: #FF7F47; /* 주황색 */
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-family: 'TitleMedium', sans-serif;
}

.btn-primary:hover {
  background-color: #FFB899; /* 주황색의 더 연한 톤 */
}
</style>
