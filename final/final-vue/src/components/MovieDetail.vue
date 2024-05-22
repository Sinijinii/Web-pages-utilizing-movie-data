<template>
    <div class="movie-details">
        <div class="poster">
            <img :src="getPosterUrl(movie.poster_path)" alt="영화 포스터">
        </div>
        <div class="details">
            <h1>{{ movie.title }}</h1>

            <div class="section">
                <h2>줄거리</h2>
                <span>{{ movie.overview }}</span>
            </div>

            <div class="section">
                <h2>장르</h2>
                <span>{{ formatGenres(movie.genres) }}</span>
            </div>

            <div class="section">
                <h2>배우</h2>
                <span>{{ formatCasts(movie.casts) }}</span>
            </div>

            <div class="section">
                <h2>OTT Platforms</h2>
                <span>{{ formatOtt(movie.ott_platforms) }}</span>
            </div>

            <div class="section">
                <h2>평점</h2>
                <span>{{ movie.vote_average }} 점</span>
            </div>
            <span>Likes :</span><span>{{ movie.likes?.length }}</span>          
          
          <button @click="toggleLike(movie)">
            {{ movie.likes?.includes(store.userId) ? 'Unlike' : 'Like' }}
          </button>
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

// 장르는 배열형식으로 받아와짐
// 장르가 비어 있다면 빈 문자열인 ''을 반환
// 아니라면 배열을 ,를 기준으로 구분하여 문자열로 반환
// 배우, 오티티도 마찬가지
function formatGenres(genres) {
    if (!genres || genres.length === 0) {
        return ''
    }
    return genres.join(', ')
}

function formatCasts(casts) {
    if (!casts || casts.length === 0) {
        return ''
    }
    return casts.join(', ')
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
.section {
    border: 1px solid #ccc;
    padding: 10px;
    margin-bottom: 10px;
}
.movie-details {
    display: flex;
    align-items: flex-start;
}

.poster {
    width: 200px;
    height: 300px;
    flex-shrink: 0;
}

.details {
    flex-grow: 1;
    margin-left: 310px;
}

span {
    font-weight: bold;
}

</style>
