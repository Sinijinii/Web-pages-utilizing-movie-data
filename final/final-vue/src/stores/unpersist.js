// import { ref, computed } from 'vue'
// import { defineStore } from 'pinia'
// import axios from 'axios'
// import { useRouter } from 'vue-router'

// export const useMovieStore = defineStore('movie', () => {


//   const loginmovies = ref()
//   const API_URL = 'http://127.0.0.1:8000'
//   const BasicPosterPath = 'https://image.tmdb.org/t/p/w500'

//   const getLoginMovies = function() {
//     axios({
//       method: 'get',
//       url: `${API_URL}/api/v1/loginmovies/`,
//       headers: {
//         Authorization: `Token ${token.value}`
//       }
//     })
//       .then(response => {
//         loginmovies.value = response.data
//       })
//       .catch(error => {
//         console.log(error)
//       })
//   }
//   return { loginmovies, getLoginMovies}
// })