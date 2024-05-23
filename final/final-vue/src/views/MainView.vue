<template>
  <div class="main-view">
    <div class="search-section">
      <div class="search-background-video">
        <video autoplay muted loop ref="backgroundVideo">
          <source :src="currentVideoSource" type="video/mp4">
        </video>
        <div class="search-box">
          <input type="text" v-model="searchTerm" placeholder="영화 제목을 입력하세요" @keyup.enter="searchMovie" />
          <img src="@/../imgs/searchicon.png" alt="Search Icon" class="search-icon" @click="searchMovie" />
        </div>
      </div>
    </div>

    <div class="buttons">
      <button v-if="store.loginmovies?.Netflix" @click="scrollToSection('netflix')">넷플릭스</button>
      <button v-if="store.loginmovies?.DisneyPlus" @click="scrollToSection('disney')">디즈니</button>
      <button v-if="store.loginmovies?.Watcha" @click="scrollToSection('watcha')">왓챠</button>
      <button @click="scrollToSection('topRate')">인기순</button>
      <button @click="scrollToSection('mostVoted')">최다 득표순</button>
      <button @click="scrollToSection('latest')">최신순</button>
    </div>
    <br>
    <br>
    <br>
    <br>

    <div v-if="store.loginmovies?.Netflix" id="netflix" class="movie-section">
      <div class="section-header">
        <img src="@/../logo/NetflixLogo.png" alt="Netflix Logo" class="logo-image">
        <h3 class="section-title">넷플릭스</h3>
      </div>
      <div class="poster-container">
        <button class="scroll-button left" @click="scrollLeft('netflixPosters')">
          <img src="@/../imgs/left.png" alt="Scroll Left" class="button-image">
        </button>
        <div class="poster-box" id="netflixPosters">
          <OttMovie :ott="store.loginmovies.Netflix" v-if="store.isLogin" />
        </div>
        <button class="scroll-button right" @click="scrollRight('netflixPosters')">
          <img src="@/../imgs/right.png" alt="Scroll Right" class="button-image">
        </button>
      </div>
    </div>
    <br>
    <br>
    <div v-if="store.loginmovies?.DisneyPlus" id="disney" class="movie-section">
      <div class="section-header">
        <img src="@/../logo/DisneyLogo.png" alt="Disney Logo" class="logo-image">
        <h3 class="section-title">디즈니</h3>
      </div>
      <div class="poster-container">
        <button class="scroll-button left" @click="scrollLeft('disneyPosters')">
          <img src="@/../imgs/left.png" alt="Scroll Left" class="button-image">
        </button>
        <div class="poster-box" id="disneyPosters">
          <OttMovie :ott="store.loginmovies.DisneyPlus" v-if="store.isLogin" />
        </div>
        <button class="scroll-button right" @click="scrollRight('disneyPosters')">
          <img src="@/../imgs/right.png" alt="Scroll Right" class="button-image">
        </button>
      </div>
    </div>
    <br>
    <br>
    <div v-if="store.loginmovies?.Watcha" id="watcha" class="movie-section">
      <div class="section-header">
        <img src="@/../logo/WatchaLogo.png" alt="Watcha Logo" class="logo-image">
        <h3 class="section-title">왓챠</h3>
      </div>
      <div class="poster-container">
        <button class="scroll-button left" @click="scrollLeft('watchaPosters')">
          <img src="@/../imgs/left.png" alt="Scroll Left" class="button-image">
        </button>
        <div class="poster-box" id="watchaPosters">
          <OttMovie :ott="store.loginmovies.Watcha" v-if="store.isLogin" />
        </div>
        <button class="scroll-button right" @click="scrollRight('watchaPosters')">
          <img src="@/../imgs/right.png" alt="Scroll Right" class="button-image">
        </button>
      </div>
    </div>
    <br>
    <br>
    <div id="topRate" class="movie-section">
      <div class="section-header">
        <h3 class="section-title">인기순</h3>
      </div>
      <div class="poster-container">
        <button class="scroll-button left" @click="scrollLeft('topRatePosters')">
          <img src="@/../imgs/left.png" alt="Scroll Left" class="button-image">
        </button>
        <div class="poster-box" id="topRatePosters">
          <TopRateMovie v-if="!loading" />
        </div>
        <button class="scroll-button right" @click="scrollRight('topRatePosters')">
          <img src="@/../imgs/right.png" alt="Scroll Right" class="button-image">
        </button>
      </div>
    </div>
    <br>
    <br>
    <div id="mostVoted" class="movie-section">
      <div class="section-header">
        <h3 class="section-title">최다 득표순</h3>
      </div>
      <div class="poster-container">
        <button class="scroll-button left" @click="scrollLeft('mostVotedPosters')">
          <img src="@/../imgs/left.png" alt="Scroll Left" class="button-image">
        </button>
        <div class="poster-box" id="mostVotedPosters">
          <MostVotedMovie v-if="!loading" />
        </div>
        <button class="scroll-button right" @click="scrollRight('mostVotedPosters')">
          <img src="@/../imgs/right.png" alt="Scroll Right" class="button-image">
        </button>
      </div>
    </div>
    <br>
    <br>
    <div id="latest" class="movie-section">
      <div class="section-header">
        <h3 class="section-title">최신순</h3>
      </div>
      <div class="poster-container">
        <button class="scroll-button left" @click="scrollLeft('latestPosters')">
          <img src="@/../imgs/left.png" alt="Scroll Left" class="button-image">
        </button>
        <div class="poster-box" id="latestPosters">
          <LatestMovie v-if="!loading" />
        </div>
        <button class="scroll-button right" @click="scrollRight('latestPosters')">
          <img src="@/../imgs/right.png" alt="Scroll Right" class="button-image">
        </button>
      </div>
    </div>
  </div>
</template>



<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useCounterStore } from '@/stores/counter'
import { useRouter } from 'vue-router'
import axios from 'axios'
import OttMovie from '@/components/OttMovie.vue'
import TopRateMovie from '@/components/TopRateMovie.vue'
import MostVotedMovie from '@/components/MostVotedMovie.vue'
import LatestMovie from '@/components/LatestMovie.vue'

const store = useCounterStore()
const searchTerm = ref('')
const router = useRouter()
const none = ref(false)

onMounted(async () => {
  await store.getMovies()
  loading.value = false
});
const loading = ref(false)
const currentVideoSource = ref('/videos/Avengers2_trailer.mp4') // 초기 동영상 소스

const videoSources = [
  '/videos/Avengers2_trailer.mp4',
  '/videos/Jurassic_World_trailer.mp4'
]

let videoIndex = 0
let videoInterval = null

function changeVideoSource() {
  videoIndex = (videoIndex + 1) % videoSources.length
  currentVideoSource.value = videoSources[videoIndex]
  const videoElement = document.querySelector('video')
  videoElement.load() // 동영상 소스 변경 후 비디오 다시 로드
}

onMounted(() => {
  videoInterval = setInterval(changeVideoSource, 10000) // 10초마다 동영상 변경
})

onUnmounted(() => {
  clearInterval(videoInterval)
})

function scrollToSection(sectionId) {
  const section = document.getElementById(sectionId)
  if (section) {
    section.scrollIntoView({ behavior: 'smooth' })
  }
}

function searchMovie() {
  if (searchTerm.value.trim() !== '') {
    loading.value = true
    axios.get(`${store.API_URL}/api/v1/searchmovie/${searchTerm.value}`)
      .then((response) => {
        router.push({ name: 'MovieDetail', params: { movieId: response.data.id } })
      })
      .catch((error) => {
        console.error(error)
      })
      .finally(() => {
        loading.value = false
      })
  } else {
    alert('영화 제목을 입력해야 합니다.')
  }
}

function scrollLeft(id) {
  const container = document.getElementById(id)
  container.scrollLeft -= 300
}

function scrollRight(id) {
  const container = document.getElementById(id)
  container.scrollLeft += 300
}

if (store.isLogin === true) {
  store.getLoginMovies()
}

console.log(store.loginmovies);
</script>




<style scoped>
@import url('@/assets/fonts/fonts.css');

.main-view {
  font-family: 'BatangRegular', Arial, sans-serif;
  background-color: #FFF6E5;
}

.search-section {
  position: relative;
  height: 700px;
  background-color: #fcfcfc;
  max-width: 100%;
}

.search-background-video {
  position: absolute;
  width: 100%;
  height: 100%;
  overflow: hidden;
  /* border-radius: 10px; */
}

.search-background-video video {
  width: 100%;
  height: 100%;
  object-fit: cover;
  /* border-radius: 10px; */
}

.search-box {
  position: absolute;
  top: 50%;
  left: 53%;
  transform: translate(-50%, -50%);
  display: flex;
  align-items: center;
  padding: 15px;
  border-radius: 10px;
}

.search-box input {
  padding: 10px;
  border-radius: 5px;
  font-size: 20px;
  margin-right: 10px;
  width: 400px;
  font-family: 'TitleLight', Arial, sans-serif;
  background-color: rgba(0, 0, 0, 0.6);
  border: none;
  color: white;
}

.search-icon {
  cursor: pointer;
  width: 30px;
  height: 30px;
}

.buttons {
  display: flex;
  justify-content: center;
  margin: 20px 0;
  margin-top: 50px;
}

.buttons button {
  padding: 10px 20px;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
  font-family: 'TitleMedium', Arial, sans-serif;
  margin: 0 30px;
  margin-top: 30px;
  background-color: orange;
}

.movie-section {
  margin: 20px 0;
}

.section-title {
  font-size: 38px;
  color: #333;
  font-family: 'TitleBold', Arial, sans-serif;
  margin-left: 10px;
}

.section-header {
  display: flex;
  align-items: center;
  margin-left: 40px;
  margin-bottom: 10px;
}

.section-header img {
  margin-right: 10px;
  width: 50px;
  height: 50px;
}

.poster-container {
  position: relative;
  display: flex;
  align-items: center;
  overflow: hidden;
  margin-bottom: 20px;
  padding-top: 20px;
  margin: 0 20px;
}

.scroll-button {
  background-color: #fff;
  border: none;
  cursor: pointer;
  padding: 0;
  border-radius: 50%;
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  z-index: 1;
}

.scroll-button.left {
  left: 3px;
}

.scroll-button.right {
  right: 44px;
}

.button-image {
  width: 36px;
  height: 36px;
}

.poster-box {
  display: flex;
  overflow-x: auto;
  scroll-behavior: smooth;
  padding: 0;
  background-color: #d4d4d4;
  border: 1px solid #ccc;
  border-radius: 5px;
  width: calc(100% - 80px);
  margin: 0 20px;
  white-space: nowrap;
  height: 330px;
}

.poster-box::-webkit-scrollbar {
  display: none;
}

.movie-container {
  display: inline-block;
  margin: 10px;
  cursor: pointer;
  border-radius: 5px;
  object-fit: cover;
  width: 200px;
  height: 300px;
}
</style>

