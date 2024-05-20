<template>
    <div>
        <h3>최다 투표 순</h3>
        <div>
            <img class="movie-container" v-for="movie in store.movies.most" :key="movie.id" :src="`${store.BasicPosterPath}${movie.poster_path}`"></img>
        </div>
    </div>
</template>

<script setup>
    import { useCounterStore } from '@/stores/counter.js'

    const store = useCounterStore()
</script>

<style scoped>
.movie-container {
  display: inline-block;
  margin: 10px;
  cursor: pointer;
  width: 100px
}
</style>