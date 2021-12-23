import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/BalanceOverview.vue')
  },
  {
    path: '/import',
    name: 'Import Transactiopns',
    component: () => import('../views/ImportCSV.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
