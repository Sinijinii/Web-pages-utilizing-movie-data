<template>
    <div>
<<<<<<< HEAD
        <div v-if="ott && ott.length" class="movie-list">
            <div v-for="movie in ott" :key="movie.id" class="movie-item">
                <img class="movie-container" :src="getPostUrl(movie.poster_path)" alt="영화 포스터"
                    @click="movetodetail(movie.id)">
            </div>
=======
        <h3 v-if="store.loginmovies">Ott별</h3>
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
        <div v-else>
            <h4>영화를 추가해 주세요</h4>
>>>>>>> c501d2a3dbb7a717512cf3b3ddc324b13fc0de0e
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
<<<<<<< HEAD
    width: 200px;
    border-radius: 5px;
    height: 300px;
    object-fit: cover;
}
</style>
=======
    width: 100px
}
</style>
>>>>>>> c501d2a3dbb7a717512cf3b3ddc324b13fc0de0e
