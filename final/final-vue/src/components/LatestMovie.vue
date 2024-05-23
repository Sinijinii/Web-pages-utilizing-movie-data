<template>
    <div>
        <!-- <h3 class="section-title">최신순</h3> -->
        <div class="movie-list">
            <img class="movie-container" v-for="movie in store.movies.latest" :key="movie.id"
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
@import url('@/assets/fonts/fonts.css');
.section-title {
    font-size: 24px;
    color: #333;
    margin-bottom: 20px;
    font-family: 'TitleBold', Arial, sans-serif;
}
.movie-list {
    display: flex;
    overflow-x: auto;
    white-space: nowrap;
    /* 한 줄로 정렬 */
}

.movie-container {
    display: inline-block;
    /* 한 줄로 정렬 */
    margin-top: 13px;
    margin-left: 15px;
    margin-right: 15px;
    cursor: pointer;
    width: 200px;
    border-radius: 5px;
    /* 모서리를 둥글게 */
}
</style>
