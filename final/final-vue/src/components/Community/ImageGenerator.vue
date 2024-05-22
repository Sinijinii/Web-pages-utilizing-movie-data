<template>
  <div class="image-generator-page">
    <div class="sidebar">
      <RouterLink :to="{ name: 'Community' }" class="sidebar-link" :class="{ active: $route.name === 'Community' }">Community</RouterLink>
      <RouterLink :to="{ name: 'UploadImage' }" class="sidebar-link" :class="{ active: $route.name === 'UploadImage' }">New Post</RouterLink>
      <RouterLink :to="{ name: 'ProfileView' }" class="sidebar-link" :class="{ active: $route.name === 'ProfileView' }">My Profile</RouterLink>
      <RouterLink :to="{ name: 'LikePostsView' }" class="sidebar-link" :class="{ active: $route.name === 'LikePostsView' }">Liked Posts</RouterLink>
      <RouterLink :to="{ name: 'FindActor' }" class="sidebar-link" :class="{ active: $route.name === 'FindActor' }">Find Actor</RouterLink>
      <RouterLink :to="{ name: 'ImageGenerator' }" class="sidebar-link" :class="{ active: $route.name === 'ImageGenerator' }">Image Generator</RouterLink>
    </div>
    <div class="image-generator">
      <div class="container py-5">
        <div class="option-container" style="margin-top: 20px">
          <!-- 옵션 선택 페이지 -->
          <div v-if="step < options.length">
            <h1 class="title-medium">{{ questions[step] }}</h1>
            <div class="options">
              <div v-for="option in options[step]" :key="option.label" class="option" :class="{ 'selected-option': selectedOptions[step] === option.value }">
                <input type="radio" :id="option.value" :value="option.value" v-model="selectedOptions[step]" class="form-check-input">
                <label :for="option.value">
                  {{ option.label }}
                </label>
              </div>
            </div>
            <button class="btn btn-primary mt-3" @click="nextStep" :disabled="!selectedOptions[step]">Next</button>
          </div>

          <!-- 결과 페이지 -->
          <div v-else>
            <p class="title-medium">All options selected!</p>
            <button v-if="!imageUrl" class="btn btn-primary mt-3" @click="submitSelections" :disabled="isLoading">Submit Selections</button>
            <div v-if="isLoading" class="mt-3">Loading...</div>
            <div v-if="imageUrl && !isLoading" class="result mt-3 text-center">
              <h2 class="title-medium">Generated Image</h2>
              <img :src="`${userstore.API_URL}/media/${imageUrl}`" alt="Generated Image" class="img-fluid" />
              <div class="mt-3 text-center">
                <button class="btn btn-success me-2" @click="showShareModal">Share</button>
                <button class="btn btn-secondary" @click="resetForm">다시하기</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 로딩 모달 -->
    <div class="modal fade" id="loadingModal" tabindex="-1" aria-labelledby="loadingModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-body text-center">
            <img :src="loadingGif" alt="Loading..." />
          </div>
        </div>
      </div>
    </div>

    <!-- 공유 모달 -->
    <div class="modal fade" id="shareModal" tabindex="-1" aria-labelledby="shareModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content" style="background-color: #FAF7F5;">
          <div class="modal-header" style="border-bottom: none;">
            <h5 class="modal-title" id="shareModalLabel">Share Your Result</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <SharePost :actorImageUrl="imageUrl" similarActor="Generated Image" />
          </div>
          <div class="modal-footer" style="border-top: none;">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onUnmounted } from 'vue';
import axios from 'axios';
import { useCommunity } from '@/stores/community';
import { useCounterStore } from '@/stores/counter';
import { useRouter } from 'vue-router';
import { Modal } from 'bootstrap';
import SharePost from '@/components/Community/ShareResult.vue';

const router = useRouter();
const store = useCommunity();
const userstore = useCounterStore();

const loadingGif = ref('');

// 랜덤으로 로딩 GIF를 선택하는 함수
const getRandomLoadingGif = () => {
  const gifs = [
    new URL('@/assets/Loading/1.gif', import.meta.url).href,
    new URL('@/assets/Loading/2.gif', import.meta.url).href,
    new URL('@/assets/Loading/3.gif', import.meta.url).href,
    new URL('@/assets/Loading/4.gif', import.meta.url).href,
    new URL('@/assets/Loading/5.gif', import.meta.url).href,
  ];
  const randomIndex = Math.floor(Math.random() * gifs.length);
  return gifs[randomIndex];
};

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
let loadingModal = null;
let shareModal = null;

const nextStep = () => {
  step.value++;
};

const submitSelections = async () => {
  isLoading.value = true; // 로딩 시작
  loadingGif.value = getRandomLoadingGif(); // 랜덤으로 로딩 GIF 선택
  const loadingModalElement = document.getElementById('loadingModal');
  loadingModal = new Modal(loadingModalElement);
  loadingModal.show();

  try {
    const response = await axios.post(`${userstore.API_URL}/articles/ImageGenerator/`, {
      keywords: selectedOptions.value
    }, {
      headers: {
        'Content-Type': 'multipart/form-data',
        'Authorization': `Token ${userstore.token}`
      }
    });
    imageUrl.value = response.data.img_url;
  } catch (error) {
    console.error(error);
  } finally {
    isLoading.value = false; // 로딩 종료
    loadingModal.hide();
  }
};

const showShareModal = () => {
  const shareModalElement = document.getElementById('shareModal');
  shareModal = new Modal(shareModalElement);
  shareModal.show();
};

const resetForm = () => {
  step.value = 0;
  selectedOptions.value = [];
  imageUrl.value = '';
};

onUnmounted(() => {
  if (loadingModal) {
    loadingModal.hide();
    document.body.classList.remove('modal-open');
    const modalBackdrop = document.querySelector('.modal-backdrop');
    if (modalBackdrop) {
      modalBackdrop.remove();
    }
  }
});
</script>

<style scoped>
@import url('@/assets/fonts/fonts.css');

.image-generator-page {
  display: flex;
}

.sidebar {
  width: 200px;
  padding: 20px;
  background-color: #4C6A58; /* 짙은 녹색 배경 */
  min-height: 100vh; /* 화면 전체 높이 */
}

.sidebar-link {
  display: block;
  color: #FFF6E5; /* 크림색 텍스트 */
  font-family: 'TitleMedium', sans-serif; /* 제목 폰트 */
  text-decoration: none;
  padding: 10px 15px;
  margin-bottom: 10px;
  border-radius: 5px;
  transition: background-color 0.3s;
}

.sidebar-link.active {
  background-color: #FF7F47; /* 활성 링크의 배경색 */
  color: #FFF; /* 활성 링크의 텍스트 색상 */
}

.sidebar-link:hover {
  background-color: #333333; /* 어두운 회색 배경 */
}

.image-generator {
  background-color: #FAF7F5; /* 전체 페이지 배경색 */
  min-height: 100vh;
  flex-grow: 1;
  display: flex;
  align-items: flex-start;
  justify-content: center;
  padding-top: 20px;
}

.container {
  background-color: #FFF6E5; /* 크림색 배경 */
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.option-container {
  text-align: center;
}

.options {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.option {
  background-color: #FFFFFF; /* 옵션 배경색 */
  border: 1px solid #4C6A58; /* 테두리 색상 */
  border-radius: 5px;
  margin: 10px 0;
  padding: 10px 20px;
  width: 80%;
  text-align: left;
  transition: background-color 0.3s;
  cursor: pointer; /* 라벨 클릭 커서 변경 */
}

.option.selected-option {
  background-color: #FF7F47; /* 선택된 옵션 배경색 */
  color: #FFF; /* 선택된 옵션 텍스트 색상 */
}

.option label {
  display: flex;
  align-items: center;
  cursor: pointer; /* 라벨 클릭 커서 변경 */
  margin: 0;
  color: inherit; /* 선택된 옵션 텍스트 색상 상속 */
  font-family: 'TitleMedium', sans-serif; /* 제목 폰트 */
  width: 100%; /* 라벨 전체 너비로 확장 */
}

.option input[type="radio"] {
  display: none; /* 라디오 버튼 숨기기 */
}

button.btn-primary {
  background-color: #FF7F47; /* 주황색 */
  border: none;
}

button.btn-primary:disabled {
  background-color: #FFB899; /* 주황색의 더 연한 톤 */
}

button.btn-success {
  background-color: #4C6A58; /* 녹색 */
  border: none;
}

button.btn-secondary {
  background-color: #333333; /* 어두운 회색 */
  border: none;
}

.result img {
  margin-top: 20px;
  max-width: 100%;
}

.modal-body img {
  max-width: 100%;
  height: auto;
  max-height: calc(100vh - 200px); /* 모달 크기에 맞게 이미지 크기 조정 */
}
</style>
