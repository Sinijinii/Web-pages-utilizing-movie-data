<template>
  <div>App.vue // navbar 사용 [RouterLink로 로고, 추천영화, game, mypage]</div>
  <!-- <RouterView /> -->
  <MainView />
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router'
import MainView from './views/MainView.vue';
</script>

<style>
</style>
