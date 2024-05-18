<template>
    <nav>
      <RouterLink :to="{ name: 'SignUpView' }">회원가입</RouterLink> |
      <RouterLink :to="{ name: 'LogInView' }">로그인</RouterLink> |
      <RouterLink :to="{ name: 'UserRecommandView' }">추천 영화</RouterLink> |
      <RouterLink :to="{ name: 'Community' }">Community</RouterLink>
    </nav>
    <RouterView />


</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router'
import MainView from './views/MainView.vue';
</script>

<style>
</style>
