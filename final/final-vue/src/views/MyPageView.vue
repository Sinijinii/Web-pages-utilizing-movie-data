<template>
  <div>
    <h1>마이페이지</h1>
    <p>{{ username }}의 페이지</p>
    <p>내가 좋아하는 영화: {{ selectedmovies }}</p>
    <p>내가 구독한 ott: {{ selectedotts }}</p>
    <!-- 회원 수정, ott, 영화 선택, 좋아하는 영화 장르 변경, 닮은꼴 찾기 링크 -->
    <button @click="moreinfo">추가 정보 수정하기</button>
  </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter'
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const store = useCounterStore()
const username = ref(route.params.username)
const selectedmovies = ref([])
const selectedotts = ref([])
const userId = ref(null)

const moreinfo = () => {
  router.push({name: 'Usermovie', params: {id: userId.value}})
}

onMounted (() => {
  axios({
  method: 'get',
  url: `${store.API_URL}/user/${username.value}`,
  headers: {
        Authorization: `Token ${store.token}`
      }
})
// 여기 수정함
.then((response) => {
  selectedmovies.value = response.data.selectedmovies
  selectedotts.value = response.data.selectedotts
  userId.value = response.data.user
}).catch((error) => {
  console.log(error)
})
})
</script>

<style scoped>
</style>