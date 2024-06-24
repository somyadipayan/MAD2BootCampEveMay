import { createRouter, createWebHashHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import RegisterPage from '../views/RegisterPage.vue'
import LoginPage from '../views/LoginPage.vue'
import AddCategory from '../views/AddCategory.vue'
import UpdateCategory from '../views/UpdateCategory.vue'
import AllCategories from '../views/AllCategories.vue'
import ImageTest from '@/views/ImageTest.vue'
import ImageGallery from '@/views/ImageGallery.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterPage
  },
  {
    path: '/imggallery',
    name: 'imggallery',
    component: ImageGallery
  },
  {
    path: '/view-cart',
    name: 'view-cart',
    component: () => import('../views/ViewCart.vue')
  },
  {
    path: '/login',
    name: 'login',
    component: LoginPage
  },
  {
    path:'/admin-report'
    ,name: 'admin-report'
    ,component: () => import('../views/AdminReport.vue')
  },
  {
    path:'/add-category',
    name: 'add-category',
    component: AddCategory
  },
  {
    path: '/imgtest',
    name: 'imgtest',
    component: ImageTest
  },
  {
    path: '/all-categories',
    name: 'all-categories',
    component: AllCategories
  },
  {
    path: '/update-category/:id',
    name: 'update-category',
    component: UpdateCategory
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
