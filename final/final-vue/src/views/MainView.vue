<template>
  <div>
    <p v-show="none">{{ store.loginmovies }}</p>
    <div class="search">
      <input type="text" v-model="searchTerm" placeholder="영화 제목을 입력하세요">
      <button @click="searchMovie">검색</button>
    </div>
    <div>
        <OttMovie v-if="store.isLogin"/>
        <TopRateMovie v-if="!loading"/>
        <MostVotedMovie v-if="!loading"/>
        <LatestMovie v-if="!loading"/>
    </div>
  </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter'
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import TopRateMovie from '@/components/TopRateMovie.vue'
import MostVotedMovie from '@/components/MostVotedMovie.vue'
import LatestMovie from '@/components/LatestMovie.vue'
import OttMovie from '@/components/OttMovie.vue'
import axios from 'axios'

const store = useCounterStore()
const loading = ref(true)
const searchTerm = ref('')
const router = useRouter()
const none = ref(false)

onMounted(async () => {
  await store.getMovies()
  loading.value = false
});

function searchMovie() {
  if (searchTerm.value.trim() !== '') {
    axios({
      method: 'get',
      url: `${store.API_URL}/api/v1/searchmovie/${searchTerm.value}`,
    })
      .then((response) => {
        router.push({ name: 'MovieDetail', params: { movieId: response.data.id } })
      })
      .catch((error) => {
        console.log(error)
      })
  } else {
    alert('영화제목 입력해야함')
  }
}

if (store.isLogin === true) {
  store.getLoginMovies()
}
</script>

<style scoped>

.search {
  border: 1px solid black;
}

</style>