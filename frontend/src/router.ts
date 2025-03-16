import { createRouter, createWebHistory } from 'vue-router'
import HomeView from './views/HomeView.vue'
import ProfileView from './views/ProfileView.vue'

const routes = [
  { path: '/', component: HomeView },
  { path: '/profile', component: ProfileView },
  { path: '/share/:telegram_id', component: ProfileView },
]

export default createRouter({
  history: createWebHistory(),
  routes,
})