<template>
  <div class="home-page">
    <!-- 轮播图 -->
    <div class="carousel-section">
      <el-carousel v-if="carousels.length > 0" height="400px" :interval="5000">
        <el-carousel-item v-for="item in carousels" :key="item.id">
          <img :src="item.image" :alt="item.title" class="carousel-image" />
          <div class="carousel-caption">
            <h3>{{ item.title }}</h3>
            <p>{{ item.description }}</p>
          </div>
        </el-carousel-item>
      </el-carousel>
      <el-empty v-else description="暂无轮播图" />
    </div>

    <!-- 快速入口 -->
    <div class="quick-links">
      <el-row :gutter="20">
        <el-col :xs="12" :sm="6" :md="6">
          <div class="link-card" @click="$router.push('/events')">
            <el-icon :size="40"><Trophy /></el-icon>
            <h3>浏览赛事</h3>
            <p>查看所有精彩赛事</p>
          </div>
        </el-col>
        <el-col :xs="12" :sm="6" :md="6">
          <div class="link-card" @click="$router.push('/announcements')">
            <el-icon :size="40"><Bell /></el-icon>
            <h3>查看公告</h3>
            <p>获取最新通知消息</p>
          </div>
        </el-col>
        <el-col :xs="12" :sm="6" :md="6">
          <div class="link-card" @click="handleProfileClick">
            <el-icon :size="40"><User /></el-icon>
            <h3>个人中心</h3>
            <p>管理我的报名信息</p>
          </div>
        </el-col>
        <el-col :xs="12" :sm="6" :md="6">
          <div class="link-card" @click="$router.push('/events')">
            <el-icon :size="40"><Star /></el-icon>
            <h3>热门赛事</h3>
            <p>查看最受欢迎赛事</p>
          </div>
        </el-col>
      </el-row>
    </div>

    <!-- 赛事推荐 -->
    <div class="hot-events">
      <div class="section-header">
        <h2>
          <el-icon><TrendCharts /></el-icon>
          赛事推荐
        </h2>
        <el-button text @click="$router.push('/events')">查看更多 <el-icon><ArrowRight /></el-icon></el-button>
      </div>
      <el-row v-if="hotEvents.length > 0" :gutter="20" v-loading="loading">
        <el-col v-for="event in hotEvents" :key="event.id" :xs="24" :sm="12" :md="8">
          <el-card class="event-card" :body-style="{ padding: '0px' }" @click="$router.push(`/events/${event.id}`)">
            <img :src="event.image || defaultEventImage" class="event-image" />
            <div class="event-content">
              <h3 class="event-title">{{ event.name }}</h3>
              <div class="event-info">
                <div class="info-item">
                  <el-icon><Calendar /></el-icon>
                  <span>{{ formatDate(event.start_time, 'YYYY-MM-DD') }}</span>
                </div>
                <div class="info-item">
                  <el-icon><Location /></el-icon>
                  <span>{{ event.location }}</span>
                </div>
                <div class="info-item">
                  <el-icon><User /></el-icon>
                  <span>{{ event.registration_count || 0 }} 人报名</span>
                </div>
                <div class="info-item">
                  <el-icon><View /></el-icon>
                  <span>{{ event.click_count || 0 }} 次浏览</span>
                </div>
                <div class="info-item" style="color: #E6A23C;">
                  <el-icon><Clock /></el-icon>
                  <span>报名截止: {{ formatDate(event.registration_end_time, 'MM-DD HH:mm') }}</span>
                </div>
              </div>
              <el-button
                type="primary"
                class="register-btn"
                @click.stop="handleRegister(event)"
                :disabled="event.is_registered"
              >
                {{ event.is_registered ? '已报名' : '立即报名' }}
              </el-button>
            </div>
          </el-card>
        </el-col>
      </el-row>
      <el-empty v-else description="暂无热门赛事" />
    </div>

    <!-- 最新公告 -->
    <div class="announcements">
      <div class="section-header">
        <h2>
          <el-icon><ChatDotRound /></el-icon>
          最新公告
        </h2>
        <el-button text @click="$router.push('/announcements')">查看更多 <el-icon><ArrowRight /></el-icon></el-button>
      </div>
      <el-card v-loading="loading">
        <el-timeline v-if="announcements.length > 0">
          <el-timeline-item
            v-for="item in announcements"
            :key="item.id"
            :timestamp="formatDate(item.created_at, 'YYYY-MM-DD HH:mm')"
            placement="top"
          >
            <el-link :underline="false" @click="handleAnnouncementClick(item)">
              {{ item.title }}
            </el-link>
          </el-timeline-item>
        </el-timeline>
        <el-empty v-else description="暂无公告" />
      </el-card>
    </div>

    <!-- 系统简介 -->
    <div class="system-intro">
      <el-card>
        <template #header>
          <div class="card-header">
            <span>关于系统</span>
          </div>
        </template>
        <div class="intro-content">
          <h3>运动赛事管理与报名系统</h3>
          <p>
            本系统是一个功能完善的体育赛事管理平台，提供赛事发布、在线报名、成绩管理、公告通知等功能。
            用户可以方便地浏览和报名参加各类体育赛事，管理员可以高效地管理赛事信息和参赛人员。
          </p>
          <el-divider />
          <el-row :gutter="40">
            <el-col :xs="24" :sm="8">
              <div class="feature-item">
                <el-icon :size="30" color="#409EFF"><Trophy /></el-icon>
                <h4>赛事管理</h4>
                <p>便捷的赛事发布与管理</p>
              </div>
            </el-col>
            <el-col :xs="24" :sm="8">
              <div class="feature-item">
                <el-icon :size="30" color="#67C23A"><Edit /></el-icon>
                <h4>在线报名</h4>
                <p>简单快速的报名流程</p>
              </div>
            </el-col>
            <el-col :xs="24" :sm="8">
              <div class="feature-item">
                <el-icon :size="30" color="#E6A23C"><DataAnalysis /></el-icon>
                <h4>成绩管理</h4>
                <p>专业的成绩记录与查询</p>
              </div>
            </el-col>
          </el-row>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import { ElMessage } from 'element-plus'
import {
  Trophy,
  Bell,
  User,
  Star,
  TrendCharts,
  ArrowRight,
  Calendar,
  Location,
  View,
  Clock,
  ChatDotRound,
  Edit,
  DataAnalysis
} from '@element-plus/icons-vue'
import { getCarouselList } from '@/api/carousel'
import { getEventList } from '@/api/event'
import { getAnnouncementList } from '@/api/announcement'
import { formatDate } from '@/utils'

const router = useRouter()
const store = useStore()

const loading = ref(false)
const carousels = ref([])
const hotEvents = ref([])
const announcements = ref([])
const defaultEventImage = 'https://via.placeholder.com/400x200?text=Event+Image'

// 获取登录状态
const isLogin = computed(() => store.getters['user/isLogin'])

// 获取轮播图数据
const fetchCarousels = async () => {
  try {
    const data = await getCarouselList({ is_active: true })
    carousels.value = data.results || data
  } catch (error) {
    console.error('获取轮播图失败:', error)
  }
}

// 获取热门赛事
const fetchHotEvents = async () => {
  loading.value = true
  try {
    const data = await getEventList({
      status: 'published',
      ordering: '-click_count',
      page_size: 6
    })
    hotEvents.value = data.results || []
  } catch (error) {
    console.error('获取热门赛事失败:', error)
    ElMessage.error('获取热门赛事失败')
  } finally {
    loading.value = false
  }
}

// 获取最新公告
const fetchAnnouncements = async () => {
  try {
    const data = await getAnnouncementList({
      status: 'published',
      page_size: 5,
      ordering: '-created_at'
    })
    announcements.value = data.results || []
  } catch (error) {
    console.error('获取公告列表失败:', error)
  }
}

// 处理个人中心点击
const handleProfileClick = () => {
  if (!isLogin.value) {
    ElMessage.warning('请先登录')
    router.push({ path: '/login', query: { redirect: '/profile' } })
    return
  }
  router.push('/profile')
}

// 处理报名
const handleRegister = (event) => {
  if (!isLogin.value) {
    ElMessage.warning('请先登录')
    router.push({ path: '/login', query: { redirect: `/events/${event.id}` } })
    return
  }
  router.push(`/events/${event.id}`)
}

// 处理公告点击
const handleAnnouncementClick = (announcement) => {
  // 可以跳转到公告详情页，暂时跳转到公告列表
  router.push('/announcements')
}

// 页面加载时获取数据
onMounted(() => {
  fetchCarousels()
  fetchHotEvents()
  fetchAnnouncements()
})
</script>

<style scoped>
.home-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

/* 轮播图样式 */
.carousel-section {
  margin-bottom: 30px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.carousel-image {
  width: 100%;
  height: 400px;
  object-fit: cover;
}

.carousel-caption {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 20px;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.7), transparent);
  color: #fff;
}

.carousel-caption h3 {
  margin: 0 0 10px 0;
  font-size: 24px;
}

.carousel-caption p {
  margin: 0;
  font-size: 14px;
  opacity: 0.9;
}

/* 快速入口样式 */
.quick-links {
  margin-bottom: 40px;
}

.link-card {
  background: #fff;
  border-radius: 8px;
  padding: 30px 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  height: 100%;
}

.link-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.link-card .el-icon {
  color: #409EFF;
  margin-bottom: 15px;
}

.link-card h3 {
  margin: 0 0 10px 0;
  font-size: 18px;
  color: #303133;
}

.link-card p {
  margin: 0;
  font-size: 14px;
  color: #909399;
}

/* 板块标题样式 */
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.section-header h2 {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0;
  font-size: 24px;
  color: #303133;
}

/* 热门赛事样式 */
.hot-events {
  margin-bottom: 40px;
}

.event-card {
  cursor: pointer;
  transition: all 0.3s;
  margin-bottom: 20px;
  border-radius: 8px;
  overflow: hidden;
}

.event-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.event-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.event-content {
  padding: 16px;
}

.event-title {
  margin: 0 0 12px 0;
  font-size: 18px;
  color: #303133;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.event-info {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 16px;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  color: #606266;
}

.info-item .el-icon {
  color: #909399;
}

.register-btn {
  width: 100%;
}

/* 最新公告样式 */
.announcements {
  margin-bottom: 40px;
}

:deep(.el-timeline-item__timestamp) {
  color: #909399;
  font-size: 13px;
}

/* 系统简介样式 */
.system-intro {
  margin-bottom: 40px;
}

.intro-content h3 {
  margin: 0 0 15px 0;
  font-size: 20px;
  color: #303133;
}

.intro-content p {
  margin: 0;
  line-height: 1.8;
  color: #606266;
  text-align: justify;
}

.feature-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 20px 0;
}

.feature-item .el-icon {
  margin-bottom: 10px;
}

.feature-item h4 {
  margin: 0 0 10px 0;
  font-size: 16px;
  color: #303133;
}

.feature-item p {
  margin: 0;
  font-size: 14px;
  color: #909399;
}

/* 响应式布局 */
@media screen and (max-width: 768px) {
  .carousel-image {
    height: 250px;
  }

  .carousel-caption h3 {
    font-size: 18px;
  }

  .section-header h2 {
    font-size: 20px;
  }

  .link-card {
    padding: 20px 15px;
    margin-bottom: 15px;
  }

  .link-card .el-icon {
    font-size: 32px;
  }

  .link-card h3 {
    font-size: 16px;
  }
}
</style>
