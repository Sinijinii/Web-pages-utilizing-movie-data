<template>
  <div>
    <h1>회원가입</h1>
    <form @submit.prevent="signUp">
      <div>
        <label for="username">username : </label>
        <input type="text" v-model.trim="username" id="username">
      </div>
      <div>
        <label for="password1">password : </label>
        <input type="password" v-model.trim="password1" id="password1">
      </div>
      <div>
        <label for="password2">password confirmation : </label>
        <input type="password" v-model.trim="password2" id="password2">
      </div>
      <div>
        <h2>선호하는 영화를 선택하세요 (최소 3개)</h2>
        <div v-for="movie in movies" :key="movie.id" class="movie-container" @click="toggleSelection(movie.id)">
          <img :src="movie.image" :alt="movie.title" :class="{'selected': selectedMovies.includes(movie.id)}" style="width: 100px; height: auto;">
        </div>
        <button type="submit">회원가입</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useCounterStore } from '@/stores/counter'

const username = ref(null) 
const password1 = ref(null)
const password2 = ref(null)
const store = useCounterStore()

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
//   나머지 영화들도 동일한 방식으로 추가
const selectedMovies = ref([]);

const toggleSelection = (movieId) => {
  const index = selectedMovies.value.indexOf(movieId);
  if (index === -1) {
    selectedMovies.value.push(movieId);
  } else {
    selectedMovies.value.splice(index, 1);
  }
};

const signUp = function () {
  if (selectedMovies.value.length < 3) {
    alert('최소 3개의 영화를 선택해주세요.');
    return;
  }

  const payload = {
    username: username.value,
    password1: password1.value,
    password2: password2.value,
    // selectedMovies: selectedMovies.value,
  };

  store.signUp(payload);
}
</script>

<style>
.movie-container {
  display: inline-block;
  margin: 10px;
  cursor: pointer;
}

.movie-container img.selected {
  border: 5px solid blue;
}
</style>