import { createRouter, createWebHistory } from 'vue-router'
import Profile from '../views/Profile.vue'
const HomeView = () => import('../views/HomeView.vue')
const LoginView = () => import('../views/LoginView.vue')
const SignupView = () => import('../views/SignupView.vue')
import DiscoverView from '../views/DiscoverView.vue'
const EditProfileView = () => import('../views/EditProfileView.vue') //maybe rename to just ProfileView
const SearchView = () => import('../views/SearchView.vue')
const MatchesView = () => import('../views/MatchesView.vue')
const MessagesView = () => import('../views/MessagesView.vue')
const FavouritesView = () => import('../views/FavouritesView.vue')

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),

  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },

    {
      path: '/discover',
      name: 'discover',
      component: DiscoverView
    },

    {
      path: '/profile',
      name: 'profile',
      component: Profile
    },

    {
      path: '/signup',
      name: 'signup',
      component: SignupView
    },

    {
      path: '/search',
      name: 'search',
      component: SearchView
    },

    {
      path: '/favourites',
      name: 'favourites',
      component: FavouritesView
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

    {
      path: '/edit-profile',
      name: 'edit-profile',
      component: EditProfileView
    },
    {
      path: '/profile/:user_id', 
      component: () => import('@/views/Profile.vue') 
    },
    {
      path: '/messages/:match_id?', 
      component: () => import('@/views/MessagesView.vue') 
    }

  ]
})

export default router