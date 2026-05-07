import { createRouter, createWebHistory } from 'vue-router'

const HomeView = () => import('../views/HomeView.vue')
//const AboutView = () => import('../views/AboutView.vue') i dont think we hv this
const LoginView = () => import('../views/LoginView.vue')
const SignupView = () => import('../views/SignupView.vue')
const EditProfileView = () => import('../views/EditProfileView.vue') //maybe rename to just ProfileView
const SearchView = () => import('../views/SearchView.vue')
const MatchesView = () => import('../views/MatchesView.vue')
const MessagesView = () => import('../views/MessagesView.vue')

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),

  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },

    /*{
      path: '/about',
      name: 'about',
      component: AboutView
    },*/

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
      path: '/search',
      name: 'search',
      component: SearchView
    },

    {
      path: '/matches',
      name: 'matches',
      component: MatchesView
    },

    {
      path: '/messages',
      name: 'messages',
      component: MessagesView
    },

    /*
    {
      path: '/:pathMatch(.*)*',
      redirect: '/login'
    }*/

  ]
})

export default router