<template>
  <div class="admin-layout">
    <el-container>
      <!-- 侧边栏 -->
      <el-aside :width="sidebarWidth" class="sidebar">
        <div class="logo">
          <el-icon :size="24"><Setting /></el-icon>
          <span v-if="!isCollapse">管理后台</span>
        </div>
        <el-menu
          :default-active="activeMenu"
          :collapse="isCollapse"
          :collapse-transition="false"
          router
          class="admin-menu"
        >
          <el-menu-item
            v-for="item in visibleMenuItems"
            :key="item.index"
            :index="item.index"
          >
            <el-icon>
              <component :is="item.icon" />
            </el-icon>
            <span>{{ item.label }}</span>
          </el-menu-item>
        </el-menu>
      </el-aside>

      <!-- 主体区域 -->
      <el-container class="main-container">
        <!-- 顶部导航 -->
        <el-header class="header">
          <div class="header-left">
            <el-icon class="collapse-icon" @click="toggleSidebar">
              <component :is="isCollapse ? 'Expand' : 'Fold'" />
            </el-icon>
            <el-breadcrumb separator="/">
              <el-breadcrumb-item :to="{ path: '/admin' }">首页</el-breadcrumb-item>
              <el-breadcrumb-item v-if="breadcrumbs.length">
                {{ breadcrumbs[0] }}
              </el-breadcrumb-item>
            </el-breadcrumb>
          </div>
          <div class="header-right">
            <el-button text @click="$router.push('/')">
              <el-icon><HomeFilled /></el-icon>
              返回前台
            </el-button>
            <el-dropdown @command="handleCommand">
              <span class="user-dropdown">
                <el-avatar :size="32">
                  <el-icon><User /></el-icon>
                </el-avatar>
                <span class="username">{{ userInfo.username }}</span>
                <el-icon class="el-icon--right"><arrow-down /></el-icon>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="profile">
                    <el-icon><User /></el-icon>个人信息
                  </el-dropdown-item>
                  <el-dropdown-item divided command="logout">
                    <el-icon><SwitchButton /></el-icon>退出登录
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </el-header>

        <!-- 内容区域 -->
        <el-main class="main-content">
          <router-view v-slot="{ Component }">
            <transition name="fade" mode="out-in">
              <component :is="Component" />
            </transition>
          </router-view>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter, useRoute } from 'vue-router'
import { ElMessageBox, ElMessage } from 'element-plus'
import {
  Setting,
  DataLine,
  User,
  Trophy,
  Document,
  Medal,
  Bell,
  Picture,
  ChatDotRound,
  HomeFilled,
  ArrowDown,
  SwitchButton,
  Ticket
} from '@element-plus/icons-vue'

const store = useStore()
const router = useRouter()
const route = useRoute()

const isCollapse = ref(false)
const userInfo = computed(() => store.getters['user/userInfo'])
const activeMenu = computed(() => route.path)

const sidebarWidth = computed(() => isCollapse.value ? '64px' : '200px')

const breadcrumbs = computed(() => {
  const meta = route.meta
  return meta.title ? [meta.title] : []
})

const toggleSidebar = () => {
  isCollapse.value = !isCollapse.value
}

const handleCommand = (command) => {
  switch (command) {
    case 'profile':
      router.push('/profile')
      break
    case 'logout':
      handleLogout()
      break
  }
}

const handleLogout = () => {
  ElMessageBox.confirm('确定要退出登录吗?', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    store.dispatch('user/logout')
    ElMessage.success('退出成功')
    router.push('/login')
  }).catch(() => {})
}

// Define your routes here
const allMenuItems = [
  { index: '/admin', label: '数据统计', icon: DataLine, allowedRoles: ['admin', 'referee'] },
  { index: '/admin/users', label: '用户管理', icon: User, allowedRoles: ['admin'] },
  { index: '/admin/events', label: '赛事管理', icon: Trophy, allowedRoles: ['admin'] },
  { index: '/admin/registrations', label: '报名管理', icon: Document, allowedRoles: ['admin'] },
  { index: '/admin/results', label: '成绩管理', icon: Medal, allowedRoles: ['admin', 'referee'] },
  { index: '/admin/referees', label: '裁判管理', icon: Ticket, allowedRoles: ['admin'] },
  { index: '/admin/announcements', label: '公告管理', icon: Bell, allowedRoles: ['admin'] },
  { index: '/admin/carousels', label: '轮播图管理', icon: Picture, allowedRoles: ['admin'] },
  { index: '/admin/feedback', label: '评论管理', icon: ChatDotRound, allowedRoles: ['admin'] }
]

// Filter menu items based on user role
const visibleMenuItems = computed(() => {
  const userType = userInfo.value.user_type
  if (!userType) return []
  return allMenuItems.filter(item =>
    !item.allowedRoles || item.allowedRoles.includes(userType)
  )
})
</script>

<style scoped>
.admin-layout {
  height: 100vh;
  overflow: hidden;
}

.el-container {
  height: 100%;
}

.sidebar {
  background: #304156;
  transition: width 0.3s;
  overflow-x: hidden;
}

.logo {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  color: #fff;
  font-size: 18px;
  font-weight: bold;
  background: rgba(0, 0, 0, 0.2);
}

.admin-menu {
  border: none;
  background: #304156;
}

.admin-menu :deep(.el-menu-item) {
  color: #bfcbd9;
}

.admin-menu :deep(.el-menu-item:hover) {
  background-color: rgba(0, 0, 0, 0.2);
  color: #fff;
}

.admin-menu :deep(.el-menu-item.is-active) {
  background-color: #409eff !important;
  color: #fff;
}

.main-container {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.header {
  background: #fff;
  border-bottom: 1px solid #e4e7ed;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 20px;
}

.collapse-icon {
  font-size: 20px;
  cursor: pointer;
  transition: all 0.3s;
}

.collapse-icon:hover {
  color: #409eff;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 20px;
}

.user-dropdown {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 5px 10px;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.user-dropdown:hover {
  background-color: #f5f7fa;
}

.username {
  font-size: 14px;
  color: #303133;
}

.main-content {
  background: #f0f2f5;
  padding: 20px;
  overflow-y: auto;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
