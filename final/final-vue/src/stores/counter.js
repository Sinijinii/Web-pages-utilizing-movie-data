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
    const { username, password1, password2, selectedMovies } = payload

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



  // SharePost부분
  const selectedFile = ref(null)
  const similarActor = ref('')
  const actorImageUrl = ref('')
  //커뮤니티
  const posts = ref([])

  const setFile = (file) => {
    selectedFile.value = file
  }

  const uploadImage = () => {
    if (!selectedFile.value) return

    const formData = new FormData()
    formData.append('image', selectedFile.value)
    console.log("adsjfkasnd");
    console.log(formData);
    axios({
      method: 'post',
      url: `${API_URL}/articles/find_similar_actor/`,
      data: formData,
      headers: {
        'Content-Type': 'multipart/form-data',
        'Authorization': `Token ${token.value}`,
      }
    })
      .then((response) => {
        similarActor.value = response.data.similar_actor
        actorImageUrl.value = response.data.img_url
        console.log('Image upload successful:', response.data)
      })
      .catch((error) => {
        console.error('Error uploading image:', error)
      })
  }

  const uploadResult = function (content, img_url) {
    const formData = new FormData()
    formData.append('content', content)
    formData.append('image', img_url)
    axios({
      method: 'post',
      url: `${API_URL}/articles/upload_result/`,
      data:formData,
      headers: {
        'Content-Type': 'multipart/form-data',
        'Authorization': `Token ${token.value}`,
      }

    })
      .then((response) => {
        console.log(response);
        alert('Post shared successfully!')
        router.push('/community')
      })
      .catch((error) => {
        console.log(error)
      })
  }



  const uploadPost = function (content) {
    const formData = new FormData()
    formData.append('content', content)
    formData.append('image', selectedFile.value)
    console.log('너 값이 있니?');
    console.log(token.value)
    axios({
      method: 'post',
      url: `${API_URL}/articles/create_post/`,
      data:formData,
      headers: {
        'Content-Type': 'multipart/form-data',
        'Authorization': `Token ${token.value}`,
      }

    })
      .then((response) => {
        console.log(response);
        alert('Post shared successfully!')
        router.push('/community')
      })
      .catch((error) => {
        console.log(error)
      })
  }



  const getPosts = async () => {
    try {
      const response = await axios.get(`${API_URL}/articles/get_posts/`)
      posts.value = response.data
    } catch (error) {
      console.error('Error fetching posts:', error)
    }
  }



  return { movies, API_URL, getMovies, signUp, logIn, token, isLogin, uploadResult,isLogin, LoginUsername,getMovies, signUp, logIn, saveinfo,
    selectedFile, similarActor, actorImageUrl, setFile, uploadImage, uploadPost, getRecommend
   }
}, { persist: true })
