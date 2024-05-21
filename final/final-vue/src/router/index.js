import { createRouter, createWebHistory } from 'vue-router'
import MainView from '@/views/MainView.vue'
import SignUpView from '@/views/SignUpView.vue'
import LogInView from '@/views/LogInView.vue'
import MyPageView from '@/views/MyPageView.vue'
import SelectView from '@/views/SelectView.vue'
import Usermovie from "@/components/Usermovie.vue"
import UserRecommandView from '@/views/UserRecommandView.vue'
import { useCounterStore } from '@/stores/counter'
import UploadImage from '@/components/Community/UploadImage.vue'
import SharePost from '@/components/Community/ShareResult.vue'
import ImageGenerator from '@/components/Community/ImageGenerator.vue'
import CommunityView from '@/views/Community/CommunityView.vue'
import ProfileView from '@/views/Community/ProfileView.vue'
import FollowingView from '@/views/Community/FollowingView.vue'
import FindActorView from '@/views/Community/FindActorView.vue'
import PostDetail from '@/views/Community/PostDetailView.vue'
import EditPost from '@/views/Community/EditPostView.vue'


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
      path: '/mypage/:id/moreinfo/movies',
      name: 'Usermovie',
      component: Usermovie
    },
    {
      path: '/mypage/:id/moreinfo',
      name: 'SelectView',
      component: SelectView
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
      path: '/share-post/:similarActor/:actorImageUrl',
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
    {
      path: '/following',
      name: 'FollowingView',
      component: FollowingView
    },
    {
      path: '/findactor',
      name: 'FindActor',
      component: FindActorView
    },
    {
      path: '/ImageGenerator',
      name: 'ImageGenerator',
      component: ImageGenerator
    },
    {
      path: '/post/:id',
      name: 'PostDetail',
      component: PostDetail
    },
    {
      path: '/post/:id/edit',
      name: 'EditPost',
      component: EditPost
    }
    
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