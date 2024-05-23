<template>
    <div>
        <h3>Ott별</h3>
        <div v-if="'Netflix' in store.loginmovies">
            <h4>Netflix</h4>
            <img class="movie-container" v-for="movie in store.loginmovies.Netflix" :key="movie.id"
                :src="`${store.BasicPosterPath}${movie.poster_path}`" @click="goToMovieDetail(movie.id)">
        </div>
        <div v-if="'Watcha' in store.loginmovies">
            <h4>Watcha</h4>
            <img class="movie-container" v-for="movie in store.loginmovies.Watcha" :key="movie.id"
                :src="`${store.BasicPosterPath}${movie.poster_path}`" @click="goToMovieDetail(movie.id)">
        </div>
        <div v-if="'DisneyPlus' in store.loginmovies">
            <h4>Disney Plus</h4>
            <img class="movie-container" v-for="movie in store.loginmovies.DisneyPlus" :key="movie.id"
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
    width: 100px
}
</style>
