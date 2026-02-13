import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/home/HomePage.vue')
  },
  {
    path: '/universities',
    name: 'UniversityList',
    component: () => import('@/views/university/UniversityList.vue')
  },
  {
    path: '/universities/:id',
    name: 'UniversityDetail',
    component: () => import('@/views/university/UniversityDetail.vue')
  },
  {
    path: '/majors',
    name: 'MajorList',
    component: () => import('@/views/major/MajorList.vue')
  },
  {
    path: '/majors/:id',
    name: 'MajorDetail',
    component: () => import('@/views/major/MajorDetail.vue')
  },
  {
    path: '/guides',
    name: 'GuideList',
    component: () => import('@/views/guide/GuideList.vue')
  },
  {
    path: '/guides/:id',
    name: 'GuideDetail',
    component: () => import('@/views/guide/GuideDetail.vue')
  },
  {
    path: '/cases',
    name: 'CaseList',
    component: () => import('@/views/case/CaseList.vue')
  },
  {
    path: '/cases/:id',
    name: 'CaseDetail',
    component: () => import('@/views/case/CaseDetail.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/user/Login.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/user/Register.vue')
  },
  {
    path: '/profile',
    name: 'UserProfile',
    component: () => import('@/views/user/Profile.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/favorites',
    name: 'Favorites',
    component: () => import('@/views/user/Favorites.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/admin',
    name: 'AdminDashboard',
    component: () => import('@/views/admin/Dashboard.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/universities',
    name: 'AdminUniversities',
    component: () => import('@/views/admin/Universities.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/majors',
    name: 'AdminMajors',
    component: () => import('@/views/admin/Majors.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/guides',
    name: 'AdminGuides',
    component: () => import('@/views/admin/Guides.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/cases',
    name: 'AdminCases',
    component: () => import('@/views/admin/Cases.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/users',
    name: 'AdminUsers',
    component: () => import('@/views/admin/Users.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  }
})

router.beforeEach(async (to, from, next) => {
  const userStore = useUserStore()
  
  // 如果有token但还没获取用户信息，先获取
  if (userStore.isAuthenticated && !userStore.userInfo) {
    try {
      await userStore.fetchUserInfo()
    } catch (e) {
      // token过期，清除后继续
    }
  }
  
  if (to.meta.requiresAuth && !userStore.isAuthenticated) {
    next('/login')
  } else if (to.meta.requiresAdmin && !userStore.isAdmin) {
    next('/')
  } else {
    next()
  }
})

export default router
