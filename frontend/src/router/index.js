import { createRouter, createWebHistory } from 'vue-router'
import { getToken } from '@/utils/auth'
import { ElMessage } from 'element-plus'

const routes = [
  // 前台路由
  {
    path: '/',
    component: () => import('@/layouts/FrontendLayout.vue'),
    children: [
      {
        path: '',
        name: 'Home',
        component: () => import('@/views/frontend/Home.vue'),
        meta: { title: '首页' }
      },
      {
        path: 'events',
        name: 'Events',
        component: () => import('@/views/frontend/Events.vue'),
        meta: { title: '赛事列表' }
      },
      {
        path: 'events/:id',
        name: 'EventDetail',
        component: () => import('@/views/frontend/EventDetail.vue'),
        meta: { title: '赛事详情' }
      },
      {
        path: 'announcements',
        name: 'Announcements',
        component: () => import('@/views/frontend/Announcements.vue'),
        meta: { title: '公告列表' }
      },
      {
        path: 'announcements/:id',
        name: 'AnnouncementDetail',
        component: () => import('@/views/frontend/AnnouncementDetail.vue'),
        meta: { title: '公告详情' }
      },
      {
        path: 'profile',
        name: 'Profile',
        component: () => import('@/views/frontend/Profile.vue'),
        meta: { title: '个人中心', requiresAuth: true }
      }
    ]
  },
  // 登录注册
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { title: '登录' }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/Register.vue'),
    meta: { title: '注册' }
  },
  // 后台管理路由
  {
    path: '/admin',
    component: () => import('@/layouts/AdminLayout.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
    children: [
      {
        path: '',
        name: 'AdminDashboard',
        component: () => import('@/views/admin/Dashboard.vue'),
        meta: { title: '管理后台' }
      },
      {
        path: 'users',
        name: 'AdminUsers',
        component: () => import('@/views/admin/Users.vue'),
        meta: { title: '用户管理' }
      },
      {
        path: 'events',
        name: 'AdminEvents',
        component: () => import('@/views/admin/Events.vue'),
        meta: { title: '赛事管理' }
      },
      {
        path: 'registrations',
        name: 'AdminRegistrations',
        component: () => import('@/views/admin/Registrations.vue'),
        meta: { title: '报名管理' }
      },
      {
        path: 'results',
        name: 'AdminResults',
        component: () => import('@/views/admin/Results.vue'),
        meta: { title: '成绩管理' }
      },
      {
        path: 'announcements',
        name: 'AdminAnnouncements',
        component: () => import('@/views/admin/Announcements.vue'),
        meta: { title: '公告管理' }
      },
      {
        path: 'carousels',
        name: 'AdminCarousels',
        component: () => import('@/views/admin/Carousels.vue'),
        meta: { title: '轮播图管理' }
      },
      {
        path: 'feedback',
        name: 'AdminFeedback',
        component: () => import('@/views/admin/Feedback.vue'),
        meta: { title: '反馈管理' }
      }
    ]
  },
  // 404页面
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFound.vue'),
    meta: { title: '页面不存在' }
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

// 路由守卫
router.beforeEach((to, from, next) => {
  // 设置页面标题
  document.title = to.meta.title ? `${to.meta.title} - 体育赛事管理系统` : '体育赛事管理系统'

  const token = getToken()
  const userInfo = JSON.parse(localStorage.getItem('userInfo') || '{}')

  // 需要登录的页面
  if (to.meta.requiresAuth) {
    if (!token) {
      ElMessage.warning('请先登录')
      next({
        path: '/login',
        query: { redirect: to.fullPath }
      })
      return
    }

    // 需要管理员权限
    if (to.meta.requiresAdmin && !userInfo.is_superuser) {
      ElMessage.error('没有访问权限')
      next('/')
      return
    }
  }

  // 已登录用户访问登录页，重定向到首页
  // 但只有在有userInfo的情况下才重定向（确保token有效）
  if ((to.path === '/login' || to.path === '/register') && token && userInfo.username) {
    next('/')
    return
  }

  next()
})

export default router
