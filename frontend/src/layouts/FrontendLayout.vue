<template>
  <div class="frontend-layout">
    <el-container>
      <!-- 顶部导航栏 -->
      <el-header class="header">
        <div class="header-content">
          <div class="logo" @click="$router.push('/')">
            <el-icon :size="28"><Trophy /></el-icon>
            <span>体育赛事管理系统</span>
          </div>
          <el-menu
            :default-active="activeMenu"
            mode="horizontal"
            :ellipsis="false"
            class="nav-menu"
            router
          >
            <el-menu-item index="/">首页</el-menu-item>
            <el-menu-item index="/events">赛事列表</el-menu-item>
            <el-menu-item index="/announcements">公告通知</el-menu-item>
          </el-menu>
          <div class="user-info">
            <template v-if="isLogin">
              <el-dropdown @command="handleCommand">
                <span class="user-dropdown">
                  <el-avatar :size="32" :src="userInfo.avatar">
                    <el-icon><User /></el-icon>
                  </el-avatar>
                  <span class="username">{{ userInfo.username }}</span>
                  <el-icon class="el-icon--right"><arrow-down /></el-icon>
                </span>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item command="profile">
                      <el-icon><User /></el-icon>个人中心
                    </el-dropdown-item>
                    <el-dropdown-item command="admin" v-if="isStaff">
                      <el-icon><Setting /></el-icon>管理后台
                    </el-dropdown-item>
                    <el-dropdown-item divided command="logout">
                      <el-icon><SwitchButton /></el-icon>退出登录
                    </el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </template>
            <template v-else>
              <el-button type="primary" @click="$router.push('/login')">登录</el-button>
              <el-button @click="$router.push('/register')">注册</el-button>
            </template>
          </div>
        </div>
      </el-header>

      <!-- 主体内容 -->
      <el-main class="main-content">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </el-main>

      <!-- 底部 -->
      <el-footer class="footer">
        <div class="footer-content">
          <p>&copy; 2024 体育赛事管理系统. All rights reserved.</p>
          <p>联系我们: support@sports.com | 电话: 400-xxx-xxxx</p>
        </div>
      </el-footer>
    </el-container>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter, useRoute } from 'vue-router'
import { ElMessageBox, ElMessage } from 'element-plus'

const store = useStore()
const router = useRouter()
const route = useRoute()

const isLogin = computed(() => store.getters['user/isLogin'])
const isStaff = computed(() => store.getters['user/isStaff'])
const userInfo = computed(() => store.getters['user/userInfo'])
const activeMenu = computed(() => route.path)

const handleCommand = (command) => {
  switch (command) {
    case 'profile':
      router.push('/profile')
      break
    case 'admin':
      router.push('/admin')
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
</script>

<style scoped>
.frontend-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.el-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.header {
  background: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 0;
  height: 60px !important;
  position: sticky;
  top: 0;
  z-index: 1000;
}

.header-content {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100%;
  padding: 0 20px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 20px;
  font-weight: bold;
  color: #409eff;
  cursor: pointer;
  transition: all 0.3s;
}

.logo:hover {
  transform: scale(1.05);
}

.nav-menu {
  flex: 1;
  border: none;
  margin: 0 40px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
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
  flex: 1;
  padding: 20px;
  background: #f5f7fa;
  min-height: calc(100vh - 180px);
}

.footer {
  background: #fff;
  border-top: 1px solid #e4e7ed;
  padding: 20px;
  text-align: center;
  height: auto !important;
}

.footer-content p {
  margin: 5px 0;
  color: #909399;
  font-size: 14px;
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
