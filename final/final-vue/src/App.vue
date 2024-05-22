<template>

  <nav>
      <RouterLink class="routerlink" v-if="store.LoginUsername" :to="{ name: 'SignUpView' }">회원가입</RouterLink> |
      <RouterLink class="routerlink" v-if="store.LoginUsername" :to="{ name: 'LogInView' }">로그인</RouterLink> |
      <RouterLink :to="{ name: 'MainView' }">메인페이지</RouterLink> |
      <RouterLink class="routerlink" v-if="store.LoginUsername" :to="{ name: 'MyPageView', params:{'username': store.LoginUsername } }">마이페이지</RouterLink> |
      <RouterLink class="routerlink" v-if="store.LoginUsername" :to="{ name: 'UserRecommendView' }">추천 영화</RouterLink> |
      <RouterLink class="routerlink" v-if="store.LoginUsername" :to="{ name: 'Community' }">Community</RouterLink>
      <form @submit.prevent="logout()">
        <button type="submit" v-if="store.isLogin">로그아웃</button>
      </form>
  </nav>
  <RouterView />

</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { useCounterStore } from '@/stores/counter'
import { useRouter } from 'vue-router';

const store = useCounterStore()
const router = useRouter()
const logout = function() {
  store.token = null
  store.loginmovies = null
  router.push({ name: 'LogInView'})
}
</script>

<style scoped>
</style>
