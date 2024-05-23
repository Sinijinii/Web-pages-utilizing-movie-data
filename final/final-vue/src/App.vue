<template>
  <div>
    <nav v-if="showNavbar" class="navbar navbar-expand bg-body-tertiary">
      <div class="container-fluid">
        <RouterLink class="navbar-brand" :to="{ name: 'MainView' }">
          <img src="../logo/MainLogo.png" alt="Main Logo" class="logo-image" />
        </RouterLink>
        <div class="collapse navbar-collapse justify-content-end" id="navbarSupportedContent">
          <ul class="navbar-nav ml-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <RouterLink class="nav-link" aria-current="page" :to="{ name: 'MainView' }">메인페이지</RouterLink>
            </li>
            <li class="nav-item" v-if="!store.isLogin">
              <RouterLink class="nav-link" :to="{ name: 'SignUpView' }">회원가입</RouterLink>
            </li>
            <li class="nav-item" v-if="!store.isLogin">
              <RouterLink class="nav-link" :to="{ name: 'LogInView' }">로그인</RouterLink>
            </li>
            <li class="nav-item" v-if="store.isLogin">
              <RouterLink class="nav-link" :to="{ name: 'MyPageView', params: { 'username': store.LoginUsername } }">마이페이지
              </RouterLink>
            </li>
            <li class="nav-item" v-if="store.isLogin">
              <RouterLink class="nav-link" :to="{ name: 'UserRecommendView' }">추천 영화</RouterLink>
            </li>
            <li class="nav-item" v-if="store.isLogin">
              <RouterLink class="nav-link" :to="{ name: 'Community' }">Community</RouterLink>
            </li>
            <li class="nav-item" v-if="store.isLogin">
              <form class="d-flex" @submit.prevent="logout()">
                <button type="submit" class="btn">로그아웃</button>
              </form>
            </li>
          </ul>
        </div>
      </div>
    </nav>
    <RouterView />
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRouter, useRoute, RouterLink, RouterView } from 'vue-router'
import { useCounterStore } from '@/stores/counter'

const store = useCounterStore()
const router = useRouter()
const route = useRoute()
const showNavbar = ref(true)

const logout = () => {
  store.token = null
  store.loginmovies = null
  store.isLogin()
  router.push({ name: 'LogInView' })
}

// 네비게이션 바 표시 여부를 경로에 따라 결정
watch(route, (newRoute) => {
  if (
    newRoute.name === 'Community' ||
    newRoute.name === 'UploadImage' ||
    newRoute.name === 'ProfileView' ||
    newRoute.name === 'FindActor' ||
    newRoute.name === 'ImageGenerator' ||
    newRoute.name === 'PostDetail' ||
    newRoute.name === 'EditPost' ||
    newRoute.name === 'SharePost' ||
    newRoute.name === 'LikePostsView'
  ) {
    showNavbar.value = false
  } else {
    showNavbar.value = true
  }
}, { immediate: true })
</script>

<style scoped>
.navbar {
  height: 70px;
  /* 네비게이션 바의 높이 조절 */
  background-color: #4C6A58 !important;
  /* 네비바 색깔 */
}

.nav-link {
  color: #fff !important;
  /* 네비게이션 바의 링크 텍스트의 글자색을 흰색으로 설정 */
}

.router-link-active {
  color: #FFA500 !important;
  /* 클릭된 네비게이션 바의 링크 텍스트 색상을 주황색으로 설정 */
}

.btn {
  background-color: #FF7F47;
  color: white;
}

.logo-image {
  width: 100px;
  /* 로고 이미지의 너비 조절 */
  height: auto;
  /* 높이는 자동 조절 */
}
</style>
