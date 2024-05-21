<template>

        <h1 class="pagetitle red-text">추천 영화 페이지</h1>

        <div>
            <h3>장르별 추천영화</h3>
            <ul>
                <li v-for="movie in genreRecommendmovie" :key="movie.id">
                    <img :src="getPostUrl(movie.poster_path)" alt="영화 포스터" @click="movetodetail(movie.movie_id)">
                    <p>{{ movie.title }}</p>
                </li>
            </ul>
        </div>


        <div>
            <h3>배우별 추천영화</h3>
            <ul>
                <li v-for="movie in castRecommendmovie" :key="movie.id">
                    <img :src="getPostUrl(movie.poster_path)" alt="영화 포스터" @click="movetodetail(movie.movie_id)">
                    <p>{{ movie.title }}</p>
                </li>
            </ul>
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
</script>

<style scoped>
</style>
