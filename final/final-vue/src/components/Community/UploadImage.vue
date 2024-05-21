<template>
  <div class="upload-container" style="margin-top: 20px">
    <!-- 이미지 선택 페이지 -->
    <div v-if="step === 0">
      <input type="file" @change="onFileChange" accept="image/*" />
      <button @click="nextStep" :disabled="!selectedFile">Next</button>
    </div>

    <!-- 글 작성 페이지 -->
    <div v-if="step === 1">
      <div class="upload-image" :style="`background-image:url(${imageURL})`"></div>
      <div class="write">
        <textarea v-model="content" class="write-box" placeholder="Write something..."></textarea>
      </div>
      <button @click="sharePost">Share</button>
    </div>

    <!-- 업로드 완료 페이지 -->
    <div v-if="step === 2">
      <p>Post shared successfully!</p>
      <router-link to="/community">Go to Community</router-link>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useCommunity } from '@/stores/community'

const store = useCommunity()

const step = ref(0)
const selectedFile = ref(null)
const imageURL = ref("")
const content = ref("")

const onFileChange = (event) => {
  const file = event.target.files[0]
  console.log('똑같은거지?');
  console.log(event.target.files[0]);
  if (file) {
    selectedFile.value = file
    imageURL.value = URL.createObjectURL(file)
    console.log(file);
    store.setFile(file)
  }

  console.log(file);
}

const nextStep = () => {
  step.value++
}

const sharePost = async () => {
  await store.uploadPost(content.value)
  step.value = 2
}
</script>



<style scoped>
.upload-container {
  text-align: center;
}

.upload-image {
  width: 100%;
  height: 450px;
  background-size: cover;
}

.write-box {
  border: none;
  width: 90%;
  height: 100px;
  padding: 15px;
  margin: auto;
  display: block;
  outline: none;
}

.upload-image {
  width: 100%;
  height: 450px;
  background: cornflowerblue;
  background-size: cover;
}
</style>
