<template>
  <nav>
    <RouterLink :to="{ name: 'SignUpView' }">회원가입</RouterLink> |
    <RouterLink :to="{ name: 'LogInView' }">로그인</RouterLink> |
    <RouterLink v-if="store.LoginUsername" :to="{ name: 'MyPageView', params:{'username': store.LoginUsername } }">마이페이지</RouterLink>

  </nav>
  <RouterView />
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { useCounterStore } from '@/stores/counter'

const store = useCounterStore()
</script>

<style>
</style>
