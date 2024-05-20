<template>
  <div>
    <header>
      <h1>추가정보 입력</h1>
      <p>좋아하는 영화나 구독한 ott를 등록해주세요</p>
    </header>
    <RouterLink :to="{name: 'Usermovie', params: {id: userId}}">좋아하는 영화</RouterLink> |
    <RouterLink>구독한 ott</RouterLink>

    <RouterView />
  </div>
</template>

<script setup>
import { RouterLink, RouterView, useRoute } from 'vue-router'
import { ref } from 'vue'

const route = useRoute()
const userId = ref(route.params.id)
</script>

<style scoped>
</style>