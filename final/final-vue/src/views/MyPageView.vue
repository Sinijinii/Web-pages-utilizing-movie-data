<template>
  <div>
    <mainbox class="container">
      <div class="row">
        <blank class="col-1 border-end"></blank>
        <div class="col-5 border-bottom header-bg">
          <h1 class="title-font my-1">{{ username }}</h1>
        </div>
        <div class="col-3 pt-2 border-bottom header-bg">
          <h3 class="title-font text-end my-1">내가 구독한 ott</h3>
        </div>
        <div class="col-2 text-start border-bottom border-end header-bg">
          <div class="ott-card" v-for="ott in selectedotts" :key="ott.id">
            <img :src="`${store.BasicPosterPath}${ott.logopath}`" class="object-fit-cover border rounded ott-small mx-1 my-1" :alt="`${ott.id}`">
          </div>
        </div>
        <blank class="col-1"></blank>
      </div>
      <div class="row my-3">
        <div class="col-1"></div>
        <div class="col-5">
          <h3 class="title-font text-start">내가 좋아요 표시한 영화</h3>
        </div>
        <div class="col-5 text-end">
          <button class="btn btn-success button-color" @click="moreinfo">추가 정보 수정하기</button>
        </div>
      </div>
      <div class="row">
        <div class="col-1"></div>
        <div class="col-10">
          <div class="row">
            <div class="col-6 col-md-4 col-lg-3 mb-4" v-for="movie in selectedmovies" :key="movie.id">
              <div class="card h-100 mb-1">
                <img :src="`${store.BasicPosterPath}${movie.poster_path}`" class="card-img-top fixed-size" :alt="`${movie.title}`">
                <div class="card-body">
                  <p class="card-text movie-font">{{ movie.title }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-1"></div>
      </div>
    </mainbox>
  </div>
</template>

<script setup>
import { useCounterStore } from '@/stores/counter'
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const store = useCounterStore()
const username = ref(route.params.username)
const selectedmovies = ref([])
const selectedotts = ref([])
const userId = ref(null)

const moreinfo = () => {
  router.push({name: 'Usermovie', params: {id: userId.value}})
}

onMounted (() => {
  axios({
  method: 'get',
  url: `${store.API_URL}/user/${username.value}`,
  headers: {
        Authorization: `Token ${store.token}`
      }
})
// 여기 수정함
.then((response) => {
  selectedmovies.value = response.data.selectedmovies
  selectedotts.value = response.data.selectedotts
  userId.value = response.data.user
}).catch((error) => {
  console.log(error)
})
})
</script>

<style scoped>

body, html {
    height: 100%;
    margin: 0;
}

.container {
    padding: 20px;
}

.card-img-top.fixed-size {
    width: 100%;
    height: 200px; /* Adjust the height as needed */
    object-fit: cover;
    /* object-fit: contain;  으로 포스터 전부 보이게 가능*/
}

.card {
    margin-bottom: 20px;
}

/* Responsive adjustments */
/* @media (max-width: 576px) {
    .col-6 {
        flex: 0 0 100%;
        max-width: 100%;
    }
}

@media (min-width: 576px) and (max-width: 768px) {
    .col-6 {
        flex: 0 0 50%;
        max-width: 50%;
    }
}

@media (min-width: 768px) and (max-width: 992px) {
    .col-md-4 {
        flex: 0 0 33.3333%;
        max-width: 33.3333%;
    }
}

@media (min-width: 992px) {
    .col-lg-3 {
        flex: 0 0 25%;
        max-width: 25%;
    }
} */

.movie-container {
  display: inline-block;
  margin: 10px;
}

.title-font {
  font-family: 'TitleBold';
}

.title {
  text-align: left;
  padding-top: 25px;
  padding-left: 25px;
}
.text-center {
  /* display: flex; */
  justify-content: center;
  align-items: center;
  text-align: center;
}

.ott-card {
  display: inline;
}

.ott-small {
  width: 50px;
}

.movie-font {
  font-family: 'TitleMedium';
}

.header-bg {
  background-color: #fff6e5;
}

.button-color {
  background-color: #FF7F47;
  border-color: #FF7F47;
}
</style>