<template>
  <div>
    <h1>영화 선택하는 곳</h1>
  </div>
  <form @submit.prevent="saveinfo">
    <div>
      <h2>선호하는 영화를 선택하세요 (최소 3개)</h2>
        <div v-for="movie in movies" :key="movie.id" class="movie-container" @click="toggleSelection(movie.id)">
          <img :src="movie.image" :alt="movie.title" :class="{'selected': selectedmovies.includes(movie.id)}" style="width: 100px; height: auto;">
        </div>
    </div>
    <button type="submit">입력</button>
  </form>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useCounterStore } from '@/stores/counter'
import axios from 'axios'


const store = useCounterStore()
const selectedmovies = ref([])
const selectedotts = ref([])
const route = useRoute()
const userId = ref(route.params.id)
const router = useRouter()
const movies = [
    { id: 496243, title: '기생충', image: "https://image.tmdb.org/t/p/w500//eRM0PykovgtK4lin1D4BUql8TBa.jpg" },
    { id: 27205, title: '인셉션', image: "https://image.tmdb.org/t/p/w500//zTgjeblxSLSvomt6F6UYtpiD4n7.jpg" },
    { id: 68721, title: '아이언맨3', image: "https://image.tmdb.org/t/p/w500//pGMfidaVkjMVHXNIl7yippnipFT.jpg" },
    { id: 19995, title: '아바타', image: "https://image.tmdb.org/t/p/w500//idvaCRXzHxiUprGBCpp7s7CSRhP.jpg" },
    { id: 635302, title: '귀멸의 칼날 : 무한열차', image: "https://image.tmdb.org/t/p/w500//mxdVTei65ymzhJlalIEtR1qSgV2.jpg" },
    { id: 296096, title: '미 비포 유', image: "https://image.tmdb.org/t/p/w500//aCnkVi4QTuc7E0d0qp0SAnRA3M0.jpg"},
    { id: 49797, title: '악마를 보았다', image: "https://image.tmdb.org/t/p/w500//xAhsrqrsMIO7YwKbLAlWatzFbgX.jpg" },
    { id: 862, title: '토이 스토리', image: "https://image.tmdb.org/t/p/w500//5ELwzkC7QY9vug20AvRFOXBzLbG.jpg"},
    { id: 122906, title: '어바웃타임', image: "https://image.tmdb.org/t/p/w500//f9CQblm419ysGBS697WUfGN0FoI.jpg" },
    { id: 372058, title: '너의 이름은', image: "https://image.tmdb.org/t/p/w500//2DJCufz3Oa703PbLjNX1pM6MCG2.jpg" },
    { id: 278, title: '쇼생크 탈출', image: "https://image.tmdb.org/t/p/w500//qV9BQZdiM8foEzDz0Ag5hGWE5qM.jpg"},
    { id: 313369, title: '라라랜드', image: "https://image.tmdb.org/t/p/w500//ad9ndytwOckyShSc0A6tx1rZRkW.jpg" },
    { id: 361743, title: '탑 건 : 매버릭', image: "https://image.tmdb.org/t/p/w500//jeqXUwNilvNqNXqAHsdwm5pEfae.jpg" },
    { id: 423, title: '피아니스트', image: "https://image.tmdb.org/t/p/w500//t7L2YDpu635qKT3ehqZxry4yvTX.jpg" },
    { id: 138843, title: '컨져링', image:"https://image.tmdb.org/t/p/w500//pWpTToZ32bG09PaZ1rvYG5mpOyV.jpg"},
    { id: 838209, title: '파묘', image: "https://image.tmdb.org/t/p/w500//tw0i3kkmOTjDjGFZTLHKhoeXVvA.jpg" },
    { id: 155, title: '다크 나이트', image: "https://image.tmdb.org/t/p/w500//9ICUbdveP56jRoMMVkXSOr3ceyV.jpg" },
    { id: 634649, title: '스파이더맨 : 노 웨이 홈', image: "https://image.tmdb.org/t/p/w500//fvqoI9r1GU2EFkc0xjZ6dKCuDVR.jpg" },
    { id: 157336, title: '인터스텔라', image: "https://image.tmdb.org/t/p/w500//zDNAeWU0PxKolEX1D8Vn1qWhGjH.jpg" },
    { id: 158445, title: '7번방의 선물', image: "https://image.tmdb.org/t/p/w500//c9TqJPm4pZCuiEXumTayoNIrBSK.jpg"}
]

const toggleSelection = (movieId) => {
  const index = selectedmovies.value.indexOf(movieId);
  if (index === -1) {
    selectedmovies.value.push(movieId)
  } else {
    selectedmovies.value.splice(index, 1)
  }
}


const saveinfo = function () {
if (selectedmovies.value.length < 3) {
  alert('최소 3개의 영화를 선택해주세요.');
  return;
}
console.log(selectedmovies.value);
axios({
  method: 'post',
  url: `${store.API_URL}/${userId.value}/saveinfo/`,
  data: {
    'selectedmovies': selectedmovies.value,
    'selectedotts': selectedotts.value
  },
  headers: {
        Authorization: `Token ${store.token}`
      }
})
.then((response) => {
  console.log(selectedmovies.value);
  router.push({name: 'MyPageView', params: {'username': store.LoginUsername}})
})
.catch((error) => {
  console.log(error)
})
}
</script>

<style scoped>
.movie-container {
  display: inline-block;
  margin: 10px;
  cursor: pointer;
}

.movie-container img.selected {
  border: 5px solid blue;
}
</style>