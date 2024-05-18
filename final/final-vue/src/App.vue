<template>
  <nav>
    <RouterLink :to="{ name: 'SignUpView' }">회원가입</RouterLink> |
    <RouterLink :to="{ name: 'LogInView' }">로그인</RouterLink>
  </nav>
  <RouterView />
  <div>App.vue // navbar 사용 [RouterLink로 로고, 추천영화, game, mypage]
    <nav>
      <RouterLink :to="{ name: 'UserRecommandView' }">추천 영화</RouterLink>
      <RouterLink :to="{ name: 'Community' }">Community</RouterLink>
    </nav>
    <RouterView />
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router'
import MainView from './views/MainView.vue';
</script>

<style>
</style>
