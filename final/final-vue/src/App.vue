<template>
  <!-- <nav class="navbar navbar-expand-lg bg-body-tertiary">
      <div class="container-fluid">
        <a class="navbar-brand" href="#">Navbar</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <a class="nav-link active" aria-current="page" href="#">Home</a>
            </li>
            <li class="nav-item">
              <RouterLink class="routerlink nav-link" v-if="store.LoginUsername" :to="{ name: 'MyPageView', params: { 'username': store.LoginUsername } }">마이페이지</RouterLink>
            </li>
            <li class="nav-item dropdown">
              <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                추천 영화
              </a>
              <ul class="dropdown-menu">
                <li><RouterLink class="routerlink dropdown-item" v-if="store.LoginUsername" :to="{ name: 'UserRecommendView' }">추천 영화</RouterLink></li>
                <li><a class="dropdown-item" href="#">Another action</a></li>
                <li><hr class="dropdown-divider"></li>
                <li><a class="dropdown-item" href="#">Something else here</a></li>
              </ul>
            </li>
            <li class="nav-item">
              <a class="nav-link disabled" aria-disabled="true">Disabled</a>
            </li>
          </ul>
          <form class="d-flex" role="search">
            <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search">
            <button class="btn btn-outline-success" type="submit">Search</button>
          </form>
        </div>
      </div>
    </nav> -->
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
