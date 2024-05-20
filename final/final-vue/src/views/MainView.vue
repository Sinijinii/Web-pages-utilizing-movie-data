<template>
  <div>
    <h1>메인 페이지</h1>
    <p>로그인 여부에 따라 페이지에 표시되는 영화가 다름</p>
    
    <TopRateMovie />
    <MostVotedMovie />
    <LatestMovie />
  </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter'
import { onMounted } from 'vue'
import TopRateMovie from '@/components/TopRateMovie.vue'
import MostVotedMovie from '@/components/MostVotedMovie.vue'
import LatestMovie from '@/components/LatestMovie.vue'

const store = useCounterStore()
onMounted(async () => {
  await store.getMovies()
  if (store.isLogin) {
  store.getLoginMovies()
}
})

</script>

<style scoped>

</style>