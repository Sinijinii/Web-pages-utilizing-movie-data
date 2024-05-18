import { createRouter, createWebHistory } from 'vue-router'
import MainView from '@/views/MainView.vue'
import SignUpView from '@/views/SignUpView.vue'
import LogInView from '@/views/LogInView.vue'
import UserRecommandView from '@/views/UserRecommandView.vue'
import UploadImage from '@/components/UploadImage.vue'
import SharePost from '@/components/SharePost.vue'
import CommunityView from '@/views/CommunityView.vue'
import ProfileView from '@/views/ProfileView.vue'
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
      path: '/recommand',
      name: 'UserRecommandView',
      component: UserRecommandView
    },
    {
      path:'/upload',
      name:'UploadImage',
      component:UploadImage
    },
    {
      path: '/share-post',
      name: 'SharePost',
      component: SharePost,
      props: true,
    },
    {
      path: '/community',
      name: 'Community',
      component: CommunityView
    },
    {
      path: '/profile',
      name: 'ProfileView',
      component: ProfileView
    },
    
    ]})
    
    router.beforeEach((to, from) => {
      const store = useCounterStore()
      // 인증되지 않은 사용자는 메인 페이지에 접근 할 수 없음
      if (to.name === 'MainView' && store.isLogin === false) {
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
