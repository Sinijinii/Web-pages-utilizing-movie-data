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
                    <span class="vote centered">{{ movie.vote_average }} / 10</span>
                </div>

                <div class="info-item">
                    <h2>장르</h2>
                    <div class="genrestext">
                        <span v-for="(genre, index) in movie.genres" :key="index">{{ genre }}</span>
                    </div>
                </div>

                <div class="info-item">
                    <h2>배우</h2>
                    <div class="caststext">
                        <span v-for="(cast, index) in movie.casts" :key="index">{{ cast }}</span>
                    </div>
                </div>

                <!-- <div class="info-item">
                    <h2>장르</h2>
                    <span class="genrestext" v-html="formatGenres(movie.genres)"></span>
                </div> -->

                <!-- <div class="info-item">
                    <h2>배우</h2>
                    <span class="caststext" v-html="formatCasts(movie.casts)"></span>
                </div> -->

            </div>
        </div>
        <div class="bottom-section">
            <div class="overview-section">
                <h2>줄거리</h2>
                <span>{{ movie.overview }}</span>
            </div>

            <div class="ott-section">
                <h2 class="otttitle">OTT Platforms</h2>
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

const toggleLike = (movie) => {
    axios({
        method: 'post',
        url: `${store.API_URL}/api/v1/detail/${movieId.value}/likes/`,
        headers: {
            'Authorization': `Token ${store.token}`
        }
    })
        .then(response => {
            store.Liked = response.data.liked
            console.log(response.data.liked);
            if (store.Liked === true) {
                movie.likes.push(store.userId)
            } else {
                const index = movie.likes.indexOf(store.userId)
                if (index > -1) {
                    movie.likes.splice(index, 1)
                }
            }
            console.log(movie.likes);
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
    margin-top: 20px; /* 네비바 아래 여백 조절 */
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
    border-radius: 5px;
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
    /* justify-content: space-between; */
    border: 1px solid #ccc;
    border-radius: 5px;
    padding: 10px;
    height: 40%;
    display: flex;
    flex-direction: column;
    
}

.votediv {
    display: flex;
    justify-content: space-between; /* 내부 요소를 좌우로 분산 정렬합니다. */
    border: 1px solid #ccc;
    padding: 10px;
    height: 40%;
    display: flex;
    font-family: 'TitleMedium';
    src: url('@/assets/fonts/Title_Medium.otf') format('opentype'),
         url('@/assets/fonts/woff/Title_Medium.woff') format('woff');
}

.centered {
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
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
    font-size: 50px;
    display: flex;
}

.genrestext {
    font-size: 23px;
    display: flex;
    flex-wrap: wrap; /* 필요 시 장르가 한 줄에 모두 표시되도록 wrap 설정 */
    gap: 40px; /* 각 장르 요소 사이의 간격을 조절합니다. */
    font-family: 'BatangRegular';
    src: url('@/assets/fonts/woff/Batang_Regular.woff') format('woff');
    justify-content: center; /* 요소들을 가운데 정렬합니다. */
}

.caststext {
        font-size: 23px;
        display: flex;
        flex-wrap: wrap; /* 필요 시 배우가 한 줄에 모두 표시되도록 wrap 설정 */
        gap: 40px; /* 각 배우 요소 사이의 간격을 조절합니다. */
        font-family: 'BatangRegular';
        src: url('@/assets/fonts/woff/Batang_Regular.woff') format('woff');
        justify-content: center; /* 요소들을 가운데 정렬합니다. */
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

.overview-section {
    border: 1px solid #ccc;
    border-radius: 5px;
    padding: 10px;
    
}
.ott-section {
    margin-top: 30px;
    border: 1px solid #ccc;
    border-radius: 5px;
    padding: 10px;
    margin-bottom: 40px;
}



.overview-section h2 {
    font-family: 'TitleMedium';
    src: url('@/assets/fonts/Title_Medium.otf') format('opentype'),
         url('@/assets/fonts/woff/Title_Medium.woff') format('woff');
}

.overview-section span {
    font-family: 'BatangRegular';
    src: url('@/assets/fonts/woff/Batang_Regular.woff') format('woff');
}

.otttitle {
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




