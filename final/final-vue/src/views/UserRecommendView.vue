<template>
    <div class="recommend-page">
        <h1 class="pagetitle">영화 추천</h1>

        <div class="section">
            <h3 class="section-title">장르별 추천영화</h3>
            <div class="poster-container">
                <button class="scroll-button left" @click="scrollLeft('genrePosters')">
                    <img src="@/../imgs/left.png" alt="Scroll Left" class="button-image">
                </button>
                <div class="poster-box" id="genrePosters">
                    <div class="movie-item" v-for="movie in genreRecommendmovie" :key="movie.id">
                        <img class="movie-container" :src="getPostUrl(movie.poster_path)" alt="영화 포스터"
                            @click="movetodetail(movie.movie_id)">
                        <p>{{ movie.title }}</p>
                    </div>
                </div>
                <button class="scroll-button right" @click="scrollRight('genrePosters')">
                    <img src="@/../imgs/right.png" alt="Scroll Right" class="button-image">
                </button>
            </div>
        </div>

        <div class="section">
            <h3 class="section-title">배우별 추천영화</h3>
            <div class="poster-container">
                <button class="scroll-button left" @click="scrollLeft('castPosters')">
                    <img src="@/../imgs/left.png" alt="Scroll Left" class="button-image">
                </button>
                <div class="poster-box" id="castPosters">
                    <div class="movie-item" v-for="movie in castRecommendmovie" :key="movie.id">
                        <img class="movie-container" :src="getPostUrl(movie.poster_path)" alt="영화 포스터"
                            @click="movetodetail(movie.movie_id)">
                        <p>{{ movie.title }}</p>
                    </div>
                </div>
                <button class="scroll-button right" @click="scrollRight('castPosters')">
                    <img src="@/../imgs/right.png" alt="Scroll Right" class="button-image">
                </button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useCounterStore } from '@/stores/counter'
import { useRouter } from 'vue-router'

const store = useCounterStore()
const genreRecommendmovie = ref([])
const castRecommendmovie = ref([])
const router = useRouter()

const movetodetail = (movieId) => {
    router.push({ name: 'MovieDetail', params: { movieId } })
}

onMounted(() => {
    store.getRecommend()
        .then(recommendmovie => {
            genreRecommendmovie.value = recommendmovie.top_10_genres_selec2
            castRecommendmovie.value = recommendmovie.top_10_casts_selec2
        })
        .catch(error => {
            console.log('추천 영화 실패:', error)
        })
})

function getPostUrl(posterPath) {
    return `https://image.tmdb.org/t/p/w500${posterPath}`
}

function scrollLeft(id) {
    const container = document.getElementById(id)
    container.scrollLeft -= 300
}

function scrollRight(id) {
    const container = document.getElementById(id)
    container.scrollLeft += 300
}
</script>

<style scoped>
@import url('@/assets/fonts/fonts.css');

.recommend-page {
    padding: 20px;
    font-family: 'BatangRegular', Arial, sans-serif;
    background-color: #FFF6E5;
}

.pagetitle {
    font-size: 36px;
    color: #ff6347;
    text-align: center;
    margin-top: 30px;
    margin-bottom: 30px;
    font-family: 'TitleBold', Arial, sans-serif;
}

.section {
    margin-bottom: 40px;
}

.section-title {
    font-size: 24px;
    color: #333;
    margin-top: 40px;
    margin-bottom: 20px;
    margin-left: 40px;
    font-family: 'TitleMedium', Arial, sans-serif;
}

.poster-container {
    display: flex;
    align-items: center;
    overflow: hidden;
    margin-bottom: 20px;
}

.scroll-button {
    background-color: #fff;
    border: none;
    cursor: pointer;
    padding: 0;
    border-radius: 50%;
    margin: 0;
}

.button-image {
    width: 30px;
    height: 30px;
}

.poster-box {
    display: flex;
    overflow-x: auto;
    overflow-y: hidden;
    scroll-behavior: smooth;
    padding: 0;
    background-color: #d4d4d4;
    border: 1px solid #ccc;
    border-radius: 5px;
    width: calc(100% - 80px);
    margin: 0 20px;
    white-space: nowrap;
    height: 380px;
}

.poster-box::-webkit-scrollbar {
    display: none;
}

.movie-item {
    display: inline-block;
    text-align: center;
    margin: 10px;
    margin-top: 20px;
    width: 200px;
}

.movie-container {
    display: block;
    margin: 0 auto;
    cursor: pointer;
    width: 200px;
    height: 300px;
    object-fit: cover;
    border-radius: 5px;
}

.movie-item p {
    font-size: 20px;
    font-weight: bold;
    color: #555;
    margin-top: 5px;
    font-family: 'BatangRegular', Arial, sans-serif;
    word-wrap: break-word;
    white-space: normal;
    height: 2.6em;
    line-height: 1.3em;
    overflow: hidden;
    text-overflow: ellipsis;
}
</style>
