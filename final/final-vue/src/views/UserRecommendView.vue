<template>
    <div class="black-background">
        <h1 class="pagetitle red-text">추천 영화 페이지</h1>

        <div class="card-container">
            <!-- 장르별 추천영화 카드 -->
            <div class="card gray-background">
                <h3 class="center">장르별 추천영화</h3>
                <div class="movie-scroll">
                    <ul class="movie-list horizontal">
                        <li v-for="movie in genreRecommendmovie" :key="movie.id">
                            <img :src="getPostUrl(movie.poster_path)" alt="영화 포스터" @click="movetodetail(movie.movie_id)">
                            <p>{{ movie.title }}</p>
                        </li>
                    </ul>
                </div>
            </div>
        </div>

        <div class="card-container">
            <!-- 배우별 추천영화 카드 -->
            <div class="card gray-background lastcard">
                <h3 class="center">배우별 추천영화</h3>
                <div class="movie-scroll">
                    <ul class="movie-list horizontal">
                        <li v-for="movie in castRecommendmovie" :key="movie.id">
                            <img :src="getPostUrl(movie.poster_path)" alt="영화 포스터" @click="movetodetail(movie.movie_id)">
                            <p>{{ movie.title }}</p>
                        </li>
                    </ul>
                </div>
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
</script>

<style scoped>
.pagetitle {
    text-align: center;
    font-weight: 700;
    /* 더 굵은 글씨 */
    color: #E50914;
    /* 넷플릭스 빨간색 */
    font-size: 2rem;
    /* 제목 크기 */
    margin: 20px 0;
    /* 상하 여백 추가 */
}

.black-background {
    background-color: #141414;
    /* 넷플릭스 배경색 */
    color: #fff;
    /* 텍스트 색상 흰색으로 변경 */
    min-height: 100vh;
    /* 최소 높이 설정 */
}

.center {
    text-align: center;
    font-weight: bold;
}

.card-container {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 20px;
}

.card {
    flex: 0 1 calc(90% - 40px);
    padding: 20px;
    border: none;
    /* 테두리 제거 */
    background-color: #222222;
    /* 카드 배경색 변경 */
    margin-bottom: 20px;
    /* 아래 여백 조정 */
    max-width: 2000px;
    border-radius: 8px;
    /* 모서리 둥글게 */
}

.movie-list {
    list-style: none;
    padding: 0;
    margin: 0;
}

.movie-list.horizontal {
    display: flex;
    overflow-x: auto;
    padding-bottom: 10px;
}

.movie-list.horizontal li {
    flex: 0 0 auto;
    margin-right: 10px;
}

.movie-list li img {
    width: 150px;
    /* 포스터 너비 조정 */
    border-radius: 4px;
    /* 포스터 모서리 둥글게 */
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
    /* 그림자 효과 추가 */
    transition: transform 0.3s ease;
    /* 부드러운 변환 효과 */
}

.movie-list li img:hover {
    transform: scale(1.05);
    /* 호버 시 확대 효과 */
}

.movie-list li p {
    text-align: center;
    font-size: 14px;
    /* 글씨 크기 조정 */
    margin-top: 5px;
    /* 위 여백 추가 */
    display: -webkit-box;
    /* Flexbox 사용 */
    -webkit-box-orient: vertical;
    /* 세로 방향 */
    -webkit-line-clamp: 2;
    /* 최대 줄 수 2줄 */
    overflow: hidden;
    /* 넘치는 텍스트 숨기기 */
    text-overflow: ellipsis;
    /* 생략 부호(...) 추가 */
    white-space: normal;
    /* 줄바꿈 허용 */
    max-width: 150px;
    /* 포스터 너비와 맞춤 */
}

.lastcard {
    margin-bottom: 20px;
}

p {
    color: #fff;
}
</style>
