import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'
import {useCounterStore} from '@/stores/counter'

export const useCommunity = defineStore('Community', () => {
  const API_URL = 'http://127.0.0.1:8000'
  const store = useCounterStore()
  const token = ref(store.token)
  const router = useRouter()
  const userId = ref()

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

  const uploadResult = (content, img_url) =>{
    console.log('토큰이다 이자식아');
    console.log(token);
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
        router.push('/community')
      })
      .catch((error) => {
        console.log('error',error)
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


  


  return {API_URL, token , uploadResult, similarActor, actorImageUrl, setFile, uploadImage, uploadPost, getPosts }
}, { persist: true })
