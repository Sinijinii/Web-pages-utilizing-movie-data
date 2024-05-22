<template>
  <div>
    <h1 class="title">마이페이지</h1>
    <mainbox class="container text-center">
      <div class="row">
        <mymovie class="col">
          <p>내가 좋아요 표시한 영화</p>
          <div class="container text-center">
            <div class="row">
              <div class="col">
                <div class="card" style="width: 18rem;" v-for="movie in selectedmovies">
                  <img src="" class="card-img-top" alt="$`{movie.poster_path}`">
                  <div class="card-body">
                    <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
                  </div>
                  <p>{{ movie }}</p>
                </div>
              </div>
            </div>
          </div>
        </mymovie>
        <div class="col">
          <p>내가 구독한 ott</p>
          <p>{{ selectedotts }}</p>
        </div>
      </div>
    </mainbox>
    <!-- 회원 수정, ott, 영화 선택, 좋아하는 영화 장르 변경, 닮은꼴 찾기 링크 -->
    <button @click="moreinfo">추가 정보 수정하기</button>
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
.title {
  font-family: 'TitleBold';

}
</style>