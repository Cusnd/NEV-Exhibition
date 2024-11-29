import { createRouter, createWebHistory } from 'vue-router'
import MainPage from '../components/MainPage.vue'
import CarManagement from '../components/CarManagement.vue'
import CommentManagement from '../components/CommentManagement.vue'
import ArticleView from '../components/ArticleView.vue'
import ArticleManagement from '../components/ArticleManagement.vue'

const routes = [
  {
    path: '/',
    name: 'MainPage',
    component: MainPage
  },
  {
    path: '/manage',
    name: 'CarManagement',
    component: CarManagement
  },
  {
    path: '/manage/comments',
    name: 'CommentManagement',
    component: CommentManagement
  },
  {
    path: '/article/:id',
    name: 'ArticleView',
    component: ArticleView
  },
  {
    path: '/manage/articles',
    name: 'ArticleManagement',
    component: ArticleManagement
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router 