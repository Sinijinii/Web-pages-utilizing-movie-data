import { createRouter, createWebHistory } from 'vue-router'
import MainView from '@/views/MainView.vue'
import SignUpView from '@/views/SignUpView.vue'
import UserRecommandView from '@/views/UserRecommandView.vue'
import UploadImage from '@/components/UploadImage.vue'
import SharePost from '@/components/SharePost.vue'
import CommunityView from '@/views/CommunityView.vue'
import ProfileView from '@/views/ProfileView.vue'


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
    }
  ]})

export default router
