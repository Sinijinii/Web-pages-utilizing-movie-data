<template>
  <div class="detail-page">
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
                :class="{ 'liked': isLiked }">
                {{ isLiked ? '' : 'Like' }}
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
                <img v-if="platform.toLowerCase() === 'netflix'" src="../../../../logo/NetflixLogo.png" alt="Netflix 로고"
                  class="ott-logo">
                <img v-else-if="platform.toLowerCase() === 'disneyplus'" src="../../../../logo/DisneyLogo.png"
                  alt="Disney 로고" class="ott-logo">
                <img v-else-if="platform.toLowerCase() === 'watcha'" src="../../../../logo/WatchaLogo.png" alt="Watcha 로고"
                  class="ott-logo">
              </div>
              <span class="platform-name">{{ platform }}</span>
            </div>
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
const isLiked = ref(false)
const movieId = ref(null)
const store = useCounterStore()
movieId.value = route.params.movieId

const getPosterUrl = function (path) {
  return `https://image.tmdb.org/t/p/w500${path}`
}

const fetchMovie = async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/api/v1/detail/${movieId.value}/`)
    movie.value = response.data
    console.log(movie.value.likes);
    console.log(store.LoginUsername);
    if (movie.value.likes.includes(store.LoginUsername)) {
        isLiked.value = true 
        } // 서버에서 받아온 is_liked 값을 설정
  } catch (error) {
    console.error('영화 정보 가져오기 실패:', error)
  }
}

const toggleLike = async (movie) => {
  try {
    const response = await axios.post(`${store.API_URL}/api/v1/detail/${movieId.value}/likes/`, {}, {
      headers: {
        'Authorization': `Token ${store.token}`
      }
    })
    store.Liked = response.data.liked
    isLiked.value = response.data.liked  // 좋아요 상태 업데이트
    if (isLiked.value) {
      movie.likes.push(store.userId)
    } else {
      const index = movie.likes.indexOf(store.userId)
      if (index > -1) {
        movie.likes.splice(index, 1)
      }
    }
  } catch (error) {
    console.error('좋아요 기능 실패했다', error)
  }
}

onMounted(() => {
  fetchMovie()
})
</script>

<style scoped>
@import url('@/assets/fonts/fonts.css');

.detail-page {
  background-color: #FFF6E5;
  padding-top: 20px;
  padding-bottom: 20px;
}

.container {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-top: 20px;
  padding: 20px;
  background-color: transparent;
  /* 컨테이너 배경 투명 */
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
  background-color: transparent;
  /* 세부 정보 배경 투명 */
}

.title-like-section {
  display: flex;
  align-items: center;
  background-color: transparent;
  /* 제목과 좋아요 섹션 배경 투명 */
}

.movie-title {
  font-size: 50px;
  font-weight: bold;
  font-family: 'TitleLight';
  src: url('@/assets/fonts/Title_Light.otf') format('opentype'),
    url('@/assets/fonts/woff/Title_Light.woff') format('woff');
  background-color: transparent;
  /* 영화 제목 배경 투명 */
}

.info-item {
  display: flex;
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 10px;
  height: 40%;
  flex-direction: column;
  background-color: #FAF7F5;;
  /* 박스 배경색 흰색 */
}

.votediv {
  display: flex;
  justify-content: space-between;
  border: 1px solid #ccc;
  padding: 10px;
  height: 40%;
  display: flex;
  font-family: 'TitleMedium';
  src: url('@/assets/fonts/Title_Medium.otf') format('opentype'),
    url('@/assets/fonts/woff/Title_Medium.woff') format('woff');
  background-color: white;
  /* 박스 배경색 흰색 */
}

.info-item h2 {
  font-family: 'TitleMedium';
  src: url('@/assets/fonts/Title_Medium.otf') format('opentype'),
    url('@/assets/fonts/woff/Title_Medium.woff') format('woff');
  background-color: transparent;
  /* 정보 항목 제목 배경 투명 */
}

.info-item span {
  font-weight: bold;
  background-color: transparent;
  /* 정보 항목 내용 배경 투명 */
}

.vote {
  font-size: 50px;
  display: flex;
  background-color: transparent;
  /* 평점 배경 투명 */
}

.centered {
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
  background-color: transparent;
  /* 가운데 정렬 배경 투명 */
}

.genrestext {
  font-size: 23px;
  display: flex;
  flex-wrap: wrap;
  gap: 40px;
  font-family: 'BatangRegular';
  src: url('@/assets/fonts/woff/Batang_Regular.woff') format('woff');
  justify-content: center;
  background-color: transparent;
  /* 장르 텍스트 배경 투명 */
}

.caststext {
  font-size: 23px;
  display: flex;
  flex-wrap: wrap;
  gap: 40px;
  font-family: 'BatangRegular';
  src: url('@/assets/fonts/woff/Batang_Regular.woff') format('woff');
  justify-content: center;
  background-color: transparent;
  /* 배우 텍스트 배경 투명 */
}

.like-section {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  background-color: transparent;
  /* 좋아요 섹션 배경 투명 */
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
  background-color: transparent;
  /* 좋아요 카운트 배경 투명 */
}

.bottom-section {
  display: flex;
  flex-direction: column;
  gap: 1px;
  background-color: transparent;
  
  /* 아래 섹션 배경 투명 */
}

.overview-section {
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 10px;
  background-color: #FAF7F5;
  /* 줄거리 섹션 배경 흰색 */
}

.ott-section {
  margin-top: 30px;
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 10px;
  margin-bottom: 40px;
  background-color:#FAF7F5;
  /* OTT 섹션 배경 흰색 */
}

.overview-section h2 {
  font-family: 'TitleMedium';
  src: url('@/assets/fonts/Title_Medium.otf') format('opentype'),
    url('@/assets/fonts/woff/Title_Medium.woff') format('woff');
  background-color: transparent;
  /* 줄거리 제목 배경 투명 */
}

.overview-section span {
  font-family: 'BatangRegular';
  src: url('@/assets/fonts/woff/Batang_Regular.woff') format('woff');
  background-color: transparent;
  /* 줄거리 내용 배경 투명 */
}

.otttitle {
  font-family: 'TitleMedium';
  src: url('@/assets/fonts/Title_Medium.otf') format('opentype'),
    url('@/assets/fonts/woff/Title_Medium.woff') format('woff');
  background-color: transparent;
  /* OTT 제목 배경 투명 */
}

.overview-section h2,
.ott-section h2 {
  font-size: 20px;
  font-weight: bold;
  background-color: transparent;
  /* 섹션 제목 배경 투명 */
}

.ott-section .ott-items {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  background-color: transparent;
  /* OTT 아이템 배경 투명 */
}

.ott-section span {
  font-weight: bold;
  font-size: 25px;
  background-color: transparent;
  /* OTT 아이템 내용 배경 투명 */
}

.ott-logo {
  width: 50px;
  height: auto;
  margin-right: 5px;
}

.ott-item {
  display: flex;
  align-items: center;
  margin-bottom: 5px;
}

.platform-name {
  margin-left: 5px;
  font-weight: bold;
  background-color: transparent;
  /* 플랫폼 이름 배경 투명 */
}
</style>
