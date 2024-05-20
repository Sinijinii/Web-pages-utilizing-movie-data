import { createRouter, createWebHistory } from 'vue-router'
import MainView from '@/views/MainView.vue'
import SignUpView from '@/views/SignUpView.vue'
import LogInView from '@/views/LogInView.vue'
import MyPageView from '@/views/MyPageView.vue'
import SelectView from '@/views/SelectView.vue'
import Usermovie from "@/components/Usermovie.vue"
import UserRecommendView from '@/views/UserRecommendView.vue'
import MovieDetail from '@/components/MovieDetail.vue'
import { useCounterStore } from '@/stores/counter'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'MainView',
      component: MainView
    },
    {
      path: '/signup',
      name: 'SignUpView',
      component: SignUpView
    },
    {
      path: '/login',
      name: 'LogInView',
      component: LogInView
    },
    {
      path: '/mypage/:username',
      name: 'MyPageView',
      component: MyPageView
    },
    {
      path: '/mypage/:id/moreinfo',
      name: 'SelectView',
      component: SelectView
    },
    {
      path: '/mypage/:id/moreinfo/movies',
      name: 'Usermovie',
      component: Usermovie
    },
    {
      path: '/recommend',
      name: 'UserRecommendView',
      component: UserRecommendView
    },
    {
      path: '/detail/:movieId',
      name: 'MovieDetail',
      component: MovieDetail
    },
  ]})

  router.beforeEach((to, from) => {
    const store = useCounterStore()
    // 인증되지 않은 사용자는 마이 페이지에 접근 할 수 없음
    if (to.name === 'MyPageView' && store.isLogin === false) {
      window.alert('로그인이 필요해요!!')
      return { name: 'LogInView' }
    }
  
    // 인증된 사용자는 회원가입과 로그인 페이지에 접근 할 수 없음
    if ((to.name === 'SignUpView' || to.name === 'LogInView') && (store.isLogin === true)) {
      window.alert('이미 로그인 했습니다.')
      return { name: 'MainView' }
    }
  })


export default router
