<template>
  <div>
    <h1>메인 페이지</h1>

    <br>

    <h3>검색창</h3>

    <br>

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
import { onMounted ,ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import TopRateMovie from '@/components/TopRateMovie.vue'
import MostVotedMovie from '@/components/MostVotedMovie.vue'
import LatestMovie from '@/components/LatestMovie.vue'
import OttMovie from '@/components/OttMovie.vue'

const store = useCounterStore()
const loading = ref(true)

// console.log(loading.value);
onMounted(async () => {
  await store.getMovies()
  loading.value = false
});

// watch(() => store.isLogin, () => {
//   store.getLoginMovies()
// })
if (store.isLogin === true) {
  store.getLoginMovies()
}
</script>

<style scoped>
</style>