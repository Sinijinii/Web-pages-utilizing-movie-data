<template>
    <div>
        <h1>{{ movie.title }}</h1>
        <h3><img :src="getPosterUrl(movie.poster_path)" alt="영화 포스터"></h3>
        <h3>줄거리 : {{ movie.overview }}</h3>
        <h3>장르 : {{ formatGenres(movie.genres) }}</h3>
        <h3>배우 : {{ formatCasts(movie.casts) }}</h3>
        <h3>오티티 : {{ formatOtt(movie.ott_platforms) }}</h3>
    </div>
</template>
  
<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const movie = ref({})
const movieId = ref(null)
movieId.value = route.params.movieId

const getPosterUrl = function (path) {
    return `https://image.tmdb.org/t/p/w500${path}`
}

onMounted(() => {
    axios({
        method: 'get',
        url: `http://127.0.0.1:8000/api/v1/detail/${movieId.value}/`,
    })
        .then(response => {
            movie.value = response.data
        })
        .catch(error => {
            console.log('영화 정보 가져오기 실패:', error)
        })
})

// 장르는 배열형식으로 받아와짐
// 장르가 비어 있다면 빈 문자열인 ''을 반환
// 아니라면 배열을 ,를 기준으로 구분하여 문자열로 반환
// 배우, 오티티도 마찬가지
function formatGenres(genres) {
    if (!genres || genres.length === 0) {
        return ''
    }
    return genres.join(', ')
}

function formatCasts(casts) {
    if (!casts || casts.length === 0) {
        return ''
    }
    return casts.join(', ')
}

function formatOtt(ott_platforms) {
    if (!ott_platforms || ott_platforms.length === 0) {
        return ''
    }
    return ott_platforms.join(', ')
}
</script>

<style scoped></style>
