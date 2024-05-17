import { createRouter, createWebHistory } from 'vue-router'
import MainView from '@/views/MainView.vue'
import SignUpView from '@/views/SignUpView.vue'
import UserRecommandView from '@/views/UserRecommandView.vue'

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
  ]})

export default router
