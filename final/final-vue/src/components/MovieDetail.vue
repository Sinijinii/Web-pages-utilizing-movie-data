<template>
    <div>
        <h1>{{ movie.title }}</h1>
        <h3><img :src="getPosterUrl(movie.poster_path)" alt="영화 포스터"></h3>
        
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
    console.log(movieId.value)
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
</script>

<style scoped></style>
