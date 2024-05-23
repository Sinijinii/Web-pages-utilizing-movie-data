<template>
    <div>
        <div v-if="ott && ott.length" class="movie-list">
            <div v-for="movie in ott" :key="movie.id" class="movie-item">
                <img class="movie-container" :src="getPostUrl(movie.poster_path)" alt="영화 포스터"
                    @click="movetodetail(movie.id)">
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, defineProps } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps({
    ott: {
        type: Array,
        default: () => []
    }
})

const router = useRouter()

const getPostUrl = (posterPath) => {
    return `https://image.tmdb.org/t/p/w500${posterPath}`
}

const movetodetail = (movieId) => {
    router.push({ name: 'MovieDetail', params: { movieId } })
}
</script>

<style scoped>
@import url('@/assets/fonts/fonts.css');

.movie-list {
    display: flex;
    overflow-x: auto;
    white-space: nowrap;
    padding-bottom: 15px;
}

.movie-container {
    display: inline-block;
    margin-top: 13px;
    margin-left: 15px;
    margin-right: 15px;
    cursor: pointer;
    width: 200px;
    border-radius: 5px;
    height: 300px;
    object-fit: cover;
}
</style>