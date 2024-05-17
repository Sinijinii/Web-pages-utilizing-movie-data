<template>
  <nav>
    <RouterLink :to="{ name: 'SignUpView' }">회원가입</RouterLink> |
    <RouterLink :to="{ name: 'LogInView' }">로그인</RouterLink>
  </nav>
  <RouterView />
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<style>
</style>
