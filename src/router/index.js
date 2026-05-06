import { createRouter, createWebHistory } from 'vue-router'

const HomeView = () => import('../views/HomeView.vue')
const AboutView = () => import('../views/AboutView.vue')
const LoginView = () => import('../views/LoginView.vue')
const SignupView = () => import('../views/SignupView.vue')
const EditProfileView = () => import('../views/EditProfileView.vue')

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),

  routes: [
    {
      path: '/',
      redirect: '/login'
    },

    {
      path: '/home',
      name: 'home',
      component: HomeView
    },

    {
      path: '/about',
      name: 'about',
      component: AboutView
    },

    {
      path: '/login',
      name: 'login',
      component: LoginView
    },

    {
      path: '/signup',
      name: 'signup',
      component: SignupView
    },

    {
      path: '/edit-profile',
      name: 'edit-profile',
      component: EditProfileView
    },

    {
      path: '/:pathMatch(.*)*',
      redirect: '/login'
    }
  ]
})

export default router