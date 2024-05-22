<template>
    <div>
        <h3>최다 투표 순</h3>
        <div>
            <img class="movie-container" v-for="movie in store.movies.most" :key="movie.id"
                :src="`${store.BasicPosterPath}${movie.poster_path}`" @click="goToMovieDetail(movie.id)">
        </div>
    </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter.js'
import { useRouter } from 'vue-router'

const store = useCounterStore()
const router = useRouter()

const goToMovieDetail = (movieId) => {
    router.push({ name: 'MovieDetail', params: { movieId } })
}
</script>

<style scoped>
.movie-container {
    display: inline-block;
    margin: 10px;
    cursor: pointer;
    width: 100px;
}
</style>
