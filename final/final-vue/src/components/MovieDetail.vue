<template>
    <div class="container">
        <div class="top-section">
            <div class="poster">
                <img :src="getPosterUrl(movie.poster_path)" alt="영화 포스터">
            </div>
            <div class="details">
                <div class="title-like-section">
                    <span class="movie-title">{{ movie.title }}</span>
                    <div class="like-section">
                        <button @click="toggleLike(movie)" class="like-button"
                            :class="{ 'liked': movie.likes?.includes(store.userId) }">
                            {{ movie.likes?.includes(store.userId) ? '' : 'Like' }}
                        </button>
                    </div>
                </div>

                <div class="info-item">
                    <h2>평점</h2>
                    <span class="vote">{{ movie.vote_average }} 점</span>
                </div>

                <div class="info-item">
                    <h2>장르</h2>
                    <span class="genrestext" v-html="formatGenres(movie.genres)"></span>
                </div>

                <div class="info-item">
                    <h2>배우</h2>
                    <span v-html="formatCasts(movie.casts)"></span>
                </div>

            </div>
        </div>
        <div class="bottom-section">
            <div class="overview-section">
                <h2>줄거리</h2>
                <span>{{ movie.overview }}</span>
            </div>

            <div class="ott-section">
                <h2>OTT Platforms</h2>
                <div class="ott-items">
                    <div v-for="(platform, index) in movie.ott_platforms" :key="index" class="ott-item">
                        <div class="ott-logo-wrapper">
                            <img v-if="platform.toLowerCase() === 'netflix'" src="../../../../logo/NetflixLogo.png"
                                alt="Netflix 로고" class="ott-logo">
                            <img v-else-if="platform.toLowerCase() === 'disneyplus'" src="../../../../logo/DisneyLogo.png"
                                alt="Disney 로고" class="ott-logo">
                            <img v-else-if="platform.toLowerCase() === 'watcha'" src="../../../../logo/WatchaLogo.png"
                                alt="Watcha 로고" class="ott-logo">
                        </div>
                        <span class="platform-name">{{ platform }}</span>
                    </div>
                </div>
            </div>

        </div>
    </div>
</template>


<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import { useCounterStore } from '@/stores/counter'

const route = useRoute()
const movie = ref({})
const movieId = ref(null)
const store = useCounterStore()
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

// function formatGenres(genres) {
//     if (!genres || genres.length === 0) {
//         return ''
//     }
//     return genres.join(', ')
// }

function formatCasts(casts) {
    if (!casts || casts.length === 0) {
        return ''
    }
    return casts.map(cast => `<span>${cast}</span><br>`).join('');
}

function formatGenres(genres) {
    if (!genres || genres.length === 0) {
        return ''
    }
    return genres.map(genres => `<span>${genres}</span><br>`).join('');
}

function formatOtt(ott_platforms) {
    if (!ott_platforms || ott_platforms.length === 0) {
        return ''
    }
    return ott_platforms.join(', ')
}

const toggleLike = (movie) => {
    axios({
        method: 'post',
        url: `${store.API_URL}/api/v1/detail/${movieId.value}/likes/`,
        headers: {
            'Authorization': `Token ${store.token}`
        }
    })
        .then(response => {
            const liked = response.data.liked
            if (liked === true) {
                movie.likes.push(store.userId)
            } else {
                const index = movie.likes.indexOf(store.userId)
                if (index > -1) {
                    movie.likes.splice(index, 1)
                }
            }
        })
        .catch(error => {
            console.error('좋아요 기능 실패했다', error)
        })
}
</script>

<style scoped>
@import url('@/assets/fonts/fonts.css');



.container {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.top-section {
    display: flex;
    gap: 20px;
}

.poster {
    width: 30%;
    height: auto;
}

.poster img {
    width: 100%;
    height: auto;
}

.details {
    display: flex;
    flex-direction: column;
    gap: 10px;
    flex: 1;
}

.title-like-section {
    display: flex;
    align-items: center;
}

.movie-title {
    font-size: 50px;
    font-weight: bold;
    font-family: 'TitleLight';
    src: url('@/assets/fonts/Title_Light.otf') format('opentype'),
         url('@/assets/fonts/woff/Title_Light.woff') format('woff');
}

.info-item {
    display: flex;
    justify-content: space-between;
    border: 1px solid #ccc;
    padding: 10px;
    height: 40%;
}

.info-item h2 {
    font-family: 'TitleMedium';
    src: url('@/assets/fonts/Title_Medium.otf') format('opentype'),
         url('@/assets/fonts/woff/Title_Medium.woff') format('woff');
}
.info-item span {
    font-weight: bold;
}

.vote {
    font-size: 28px;
}

.genrestext {
    font-size: 28px;
}

.like-section {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px;
}

.like-button {
    padding: 5px 10px;
    font-size: 16px;
    background-color: transparent;
    border: none;
    cursor: pointer;
    background-image: url('../../../../imgs/sosoicon.png');
    background-size: contain;
    background-repeat: no-repeat;
    width: 50px;
    height: 50px;
    text-indent: -9999px;
    /* 텍스트 숨기기 */
}

.like-button.liked {
    background-image: url('../../../../imgs/goodicon.png');
}

.like-count {
    font-size: 16px;
}

.bottom-section {
    display: flex;
    flex-direction: column;
    gap: 1px;
}

.overview-section,
.ott-section {
    margin-top: 20px;
    border: 1px solid #ccc;
    padding: 10px;
}

.overview-section h2 {
    font-family: 'TitleMedium';
    src: url('@/assets/fonts/Title_Medium.otf') format('opentype'),
         url('@/assets/fonts/woff/Title_Medium.woff') format('woff');
}

.overview-section h2,
.ott-section h2 {
    font-size: 20px;
    font-weight: bold;
}

.ott-section .ott-items {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
}

.ott-section span {
    font-weight: bold;
    font-size: 25px;
}

.ott-logo {
    width: 50px;
    /* 로고의 너비 조정 */
    height: auto;
    /* 높이 자동 조정 */
    margin-right: 5px;
    /* 로고와 플랫폼 이름 사이의 간격 조정 */
}

.ott-item {
    display: flex;
    align-items: center;
    margin-bottom: 5px;
    /* 로고와 플랫폼 이름 사이의 간격 조정 */
}

.platform-name {
    margin-left: 5px;
    /* 로고와 플랫폼 이름 사이의 간격 조정 */
    font-weight: bold;
}
</style>




