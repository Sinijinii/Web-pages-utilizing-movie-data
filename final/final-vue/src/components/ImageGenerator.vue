<template>
    <div class="option-container" style="margin-top: 20px">
      <!-- 옵션 선택 페이지 -->
      <div v-if="step < options.length">
        <h1>Option {{ step + 1 }}</h1>
        <div v-for="option in options[step]" :key="option.label">
          <label>
            <input type="radio" :value="option.value" v-model="selectedOptions[step]">
            {{ option.label }}
          </label>
        </div>
        <button @click="nextStep" :disabled="!selectedOptions[step]">Next</button>
      </div>
  
      <!-- 결과 페이지 -->
      <div v-else>
        <p>All options selected!</p>
        <button @click="submitSelections" :disabled="isLoading">Submit Selections</button>
        <div v-if="isLoading">Loading...</div>
        <div v-if="imageUrl && !isLoading">
          <h2>Generated Image</h2>
          <img :src="`${store.API_URL}${imageUrl}`" alt="Generated Image" />
          <button @click="ShareResult">Share</button>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import axios from 'axios';
  import { useCounterStore } from '@/stores/counter';
  import {useRouter} from 'vue-router';

  const router = useRouter()
  const store = useCounterStore()

  // options 배열 정의
  const options = [
    [
        { label: '여자', value: '여자' },
        { label: '남자', value: '남자' }
    ],
    [
        { label: '나는 활발하다', value: '활발' },
        { label: '나는 차분하다', value: '차분' }
    ],
    [
        { label: '무슨 일이 생겼을 때 나는 가서 무슨 일이 있는지 본다', value: '히어로' },
        { label: '무슨 일이 생겼을 때 나는 그냥 갈 길 간다', value: '사람' }
    ],
    [
        { label: '나는 힘이 세다', value: '근육질' },
        { label: '나는 힘이 약한 편이다', value: '평균적인 몸' }
    ],
    [
        { label: '나는 로맨스를 좋아한다', value: '로맨스물' },
        { label: '나는 히어로물을 좋아한다', value: '히어로물' },
        { label: '나는 공포를 좋아한다', value: '공포' },
    ],
    [
        { label: '나는 조용한 장소를 좋아한다.', value: '조용한 실내' },
        { label: '나는 사람이 많은 곳을 좋아한다.', value: '주변에 사람이 많은 곳' },
    ],
    [
        { label: '나는 생각이 많은 편이다.', value: '배경은 신비롭고' },
        { label: '나는 생각이 많지 않다.', value: '배경은 단조롭고' },
    ],
    [
        { label: '나는 동물이 좋다.', value: '동물 캐릭터가 함께 있다.' },
        { label: '나는 사람이 좋다.', value: '동물 캐릭터는 없다.' },
    ],
  ];
  
  const step = ref(0); // 현재 단계
  const selectedOptions = ref([]); // 선택된 옵션들
  const imageUrl = ref('') //이미지 저장할 곳
  const isLoading = ref(false); // 로딩 상태

  const nextStep = () => {
    step.value++;
  };

  console.log(selectedOptions);
 
  const submitSelections = async () => {
    isLoading.value = true; // 로딩 시작
    console.log(selectedOptions.value);
    axios({
        method:'post',
        url: `${store.API_URL}/articles/ImageGenerator/`,
        data:{
            keywords: selectedOptions.value
        },
        headers: {
            'Content-Type': 'multipart/form-data',
            'Authorization': `Token ${store.token}`
        }
    })
    .then((response)=>{
        imageUrl.value =response.data.img_url
    })
    .catch((error) => {
        console.log(error)
    })
    .finally(()=>{
        isLoading.value = false; // 로딩 종료
    })
  };

  const ShareResult = () => {
    router.push({
        name: 'SharePost',
        params: {
            similarActor:'결과 이미지',
            actorImageUrl: imageUrl.value,
        }
    })
    }


  </script>
  
  <style scoped>
  .option-container {
    text-align: center;
  }
  
  .option-container h1 {
    margin-bottom: 20px;
  }
  
  .option-container label {
    display: block;
    margin: 10px 0;
  }
  
  .option-container button {
    margin-top: 20px;
  }
  
  .option-container img {
    margin-top: 20px;
    max-width: 100%;
  }
  </style>