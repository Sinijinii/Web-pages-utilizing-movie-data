<template>
  <div class="option-container" style="margin-top: 20px">
    <!-- 옵션 선택 페이지 -->
    <div v-if="step < options.length">
      <h1>{{ questions[step] }}</h1>
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
        <img :src="`${store.API_URL}/media/${imageUrl}`" alt="Generated Image" />
        <button @click="ShareResult">Share</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useCommunity } from '@/stores/community';
import {useCounterStore} from '@/stores/counter'
import { useRouter } from 'vue-router';

const router = useRouter();
const store = useCommunity();
const userstore = useCounterStore()

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
    { label: '캐주얼', value: '캐주얼' },
    { label: '정장', value: '정장' },
    { label: '스포츠웨어', value: '스포츠웨어' },
    { label: '힙한 스타일', value: '힙한 스타일' }
  ],
  [
    { label: '도시', value: '도시' },
    { label: '자연', value: '자연' },
    { label: '집', value: '집' },
    { label: '카페', value: '카페' }
  ],
  [
    { label: '학생', value: '학생' },
    { label: '직장인', value: '직장인' },
    { label: '예술가', value: '예술가' },
    { label: '자영업자', value: '자영업자' },
    { label: '기타', value: '기타' }
  ],
  [
    { label: '운동', value: '운동' },
    { label: '독서', value: '독서' },
    { label: '게임', value: '게임' },
    { label: '요리', value: '요리' },
    { label: '음악', value: '음악' },
    { label: '여행', value: '여행' }
  ],
  [
    { label: '액션', value: '액션' },
    { label: '로맨스', value: '로맨스' },
    { label: '코미디', value: '코미디' },
    { label: '드라마', value: '드라마' },
    { label: '공포', value: '공포' },
    { label: 'SF', value: 'SF' }
  ],
  [
    { label: 'N', value: 'N' },
    { label: 'S', value: 'S' }
  ]
];

// 각 단계의 질문 정의
const questions = [
  '성별을 선택해 주세요',
  '당신의 성격을 선택해 주세요',
  '주로 어떤 옷을 즐겨 입나요?',
  '주로 어디에서 시간을 보내시나요?',
  '당신의 직업은 무엇인가요?',
  '당신의 취미는 무엇인가요?',
  '선호하는 영화 장르는 무엇인가요?',
  '당신의 MBTI중 인식기능(감각-S / 직관(N))은 무엇인가요?'
];

const step = ref(0); // 현재 단계
const selectedOptions = ref([]); // 선택된 옵션들
const imageUrl = ref(''); // 이미지 저장할 곳
const isLoading = ref(false); // 로딩 상태

const nextStep = () => {
  step.value++;
};

console.log(selectedOptions);

const submitSelections = async () => {
  isLoading.value = true; // 로딩 시작
  console.log(selectedOptions.value);
  axios({
    method: 'post',
    url: `${userstore.API_URL}/articles/ImageGenerator/`,
    data: {
      keywords: selectedOptions.value
    },
    headers: {
      'Content-Type': 'multipart/form-data',
      'Authorization': `Token ${userstore.token}`
    }
  })
    .then((response) => {
      console.log('sadjkfnakdsjfnba');
      console.log(response.data);
      imageUrl.value = response.data.img_url;
      console.log(imageUrl);
    })
    .catch((error) => {
      console.log(error);
    })
    .finally(() => {
      isLoading.value = false; // 로딩 종료
    });
};

const ShareResult = () => {
  router.push({
    name: 'SharePost',
    params: {
      similarActor: '결과 이미지',
      actorImageUrl: imageUrl.value
    }
  });
};
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
