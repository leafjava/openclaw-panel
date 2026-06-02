import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'dashboard',
      component: () => import('@/views/DashboardView.vue'),
    },
    {
      path: '/github',
      name: 'github',
      component: () => import('@/views/GitHubView.vue'),
    },
    {
      path: '/news',
      name: 'news',
      component: () => import('@/views/NewsView.vue'),
    },
    {
      path: '/twitter',
      name: 'twitter',
      component: () => import('@/views/TwitterView.vue'),
    },
  ],
})

export default router
