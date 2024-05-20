import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'

export const useCounterStore = defineStore('counter', () => {
  const movies = ref([])
  const API_URL = 'http://127.0.0.1:8000'
  const token = ref(null)
  const LoginUsername = ref(null)
  const router = useRouter()


  // //추천영화 받아오는 함수
  // const getRecommend = () => {
  //   return axios.get(`${API_URL}/api/v1/recommend/`)
  //     .then(response => {
  //       return response.data
  //     })
  //     .catch(error => {
  //       console.log(error)
  //       return Promise.reject(error)
  //     })
  // }

  //추천영화 받아오는 함수
  const getRecommend = () => {
    return axios({
      method: 'get',
      url: `${API_URL}/api/v1/recommend/`,
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
      .then(response => {
        return response.data
      })
      .catch(error => {
        console.log(error)
        return Promise.reject(error)
      })
  }

// 로그인 여부
  const isLogin = computed(() => {
    if (token.value === null) {
      return false
    } else {
      return true
    }
  })

// 영화목록 불러오기
  const getMovies = function () {
    axios({
      method: 'get',
      url: `${API_URL}/api/v1/movies/`,
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
      .then(response => {
        movies.value = response.data
      })
      .catch(error => {
        console.log(error)
      })
  }

// 회원가입
  const signUp = function (payload) {
    // 1. 사용자 입력 데이터를 받아
    const { username, password1, password2 } = payload

    // 2. axios로 django에 요청을 보냄
    axios({
      method: 'post',
      url: `${API_URL}/accounts/signup/`,
      data: {
        username, password1, password2
      }
    })
     .then((response) => {
        console.log('회원가입 성공!')
    // 선택한 영화를 저장
        const password = password1
        logIn({ username, password })
       })
       .catch((error) => {
         console.log(error)
       })
  }

// 유저 정보저장
  const saveinfo = function (selectedMovies) {
    for (const movie of selectedMovies) {
      console.log(movie)
      axios({
        method: 'post',
        url: `${API_URL}/${LoginUsername.value}/saveinfo/`,
        data: { movie },
        headers: {
          Authorization: `Token ${token}`
        }
      })
      .then((response) => {
        console.log('데이터 저장 성공')
      })
      .catch((error) => {
        console.log('데이터 저장 실패');
      })
    }
  }

// 로그인
  const logIn = function (payload) {
    // 1. 사용자 입력 데이터를 받아
    const { username, password } = payload
    // 2. axios로 django에 요청을 보냄
    axios({
      method: 'post',
      url: `${API_URL}/accounts/login/`,
      data: {
        username, password
      }
    })
    .then((response) => {
      // 3. 로그인 성공 후 응답 받은 토큰을 저장
        LoginUsername.value = username
        token.value = response.data.key
        console.log(token.value);
        router.push({ name : 'MainView' })
      })
      .catch((error) => {
        console.log(error)
      })
  }
  return { movies, API_URL, token, isLogin, LoginUsername, getMovies, signUp, logIn, saveinfo, getRecommend }
}, { persist: true })
