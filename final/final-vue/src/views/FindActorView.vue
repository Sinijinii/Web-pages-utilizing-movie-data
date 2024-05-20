<template>
  <div class="upload-image">
    <h1>Find Similar Actor</h1>
    <input type="file" @change="onFileChange" accept="image/*" />
    <button @click="uploadImage" :disabled="!selectedFile">Upload</button>
    
    <div v-if="similarActor" class="result">
      <h2>{{ similarActor }}</h2>
      <img :src="actorImageUrl" alt="Similar Actor Image" v-if="actorImageUrl" />
      <button @click="ShareResult">Share</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import {useRouter} from 'vue-router';
import { useCounterStore } from '@/stores/counter'

const store = useCounterStore()
const router = useRouter()
const selectedFile = ref(null)
const similarActor = ref(null)
let actorImageUrl = ref(null)

const onFileChange = (event) => {
  selectedFile.value = event.target.files[0]
};

const uploadImage = async () => {
  if (!selectedFile.value) return

  const formData = new FormData()
  formData.append('image', selectedFile.value)

  try {
    const response = await axios.post(`${store.API_URL}/articles/find_similar_actor/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    console.log(response);
    similarActor.value = response.data.similar_actor
    actorImageUrl.value = response.data.img_url

    console.log('이미지 주소는')
    console.log(actorImageUrl)

  } catch (error) {
    console.error('Error uploading image:', error)
  }
}


const ShareResult = () => {
  router.push({
    name: 'SharePost',
    params: {
      similarActor: similarActor.value,
      actorImageUrl: actorImageUrl.value,
    }
  })
}
</script>

<style scoped>
.upload-image {
  text-align: center;
  margin-top: 50px;
}

.result {
  margin-top: 20px;
}
.result img {
  max-width: 200px;
  margin-top: 10px;
}
</style>
