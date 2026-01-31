<template>
  <div class="events-page">
    <!-- 搜索和筛选区域 -->
    <el-card class="filter-card">
      <el-row :gutter="20">
        <el-col :xs="24" :sm="12" :md="8">
          <el-input
            v-model="searchKeyword"
            placeholder="搜索赛事名称"
            clearable
            @clear="handleSearch"
            @keyup.enter="handleSearch"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
            <template #append>
              <el-button :icon="Search" @click="handleSearch">搜索</el-button>
            </template>
          </el-input>
        </el-col>
        <el-col :xs="24" :sm="12" :md="8">
          <el-select v-model="filterStatus" placeholder="选择状态" clearable @change="handleSearch">
            <el-option label="全部赛事" value="" />
            <el-option label="报名中" value="registration" />
            <el-option label="进行中" value="ongoing" />
            <el-option label="已结束" value="finished" />
          </el-select>
        </el-col>
        <el-col :xs="24" :sm="12" :md="8">
          <el-select v-model="orderBy" placeholder="排序方式" @change="handleSearch">
            <el-option label="最新发布" value="-created_at" />
            <el-option label="最热门" value="-click_count" />
            <el-option label="报名人数最多" value="-registration_count" />
            <el-option label="开始时间" value="start_time" />
          </el-select>
        </el-col>
      </el-row>
    </el-card>

    <!-- 赛事列表 -->
    <div class="events-list" v-loading="loading">
      <el-row v-if="events.length > 0" :gutter="20">
        <el-col
          v-for="event in events"
          :key="event.id"
          :xs="24"
          :sm="12"
          :md="8"
        >
          <el-card class="event-card" :body-style="{ padding: '0px' }" @click="goToDetail(event.id)">
            <div class="event-image-wrapper">
              <img :src="event.image || defaultEventImage" class="event-image" />
              <div class="event-status-badge" :class="getStatusClass(event)">
                {{ getStatusText(event) }}
              </div>
            </div>
            <div class="event-content">
              <h3 class="event-title" :title="event.name">{{ event.name }}</h3>
              <div class="event-info">
                <div class="info-item">
                  <el-icon><Calendar /></el-icon>
                  <span>{{ formatDate(event.start_time, 'YYYY-MM-DD') }}</span>
                </div>
                <div class="info-item">
                  <el-icon><Location /></el-icon>
                  <span>{{ event.location }}</span>
                </div>
                <div class="info-item" style="color: #E6A23C;">
                  <el-icon><Clock /></el-icon>
                  <span>截止: {{ formatDate(event.registration_end_time, 'MM-DD HH:mm') }}</span>
                </div>
              </div>
              <div class="event-stats">
                <div class="stat-item">
                  <el-icon><User /></el-icon>
                  <span>{{ event.registration_count || 0 }} 人报名</span>
                </div>
                <div class="stat-item">
                  <el-icon><View /></el-icon>
                  <span>{{ event.click_count || 0 }} 次浏览</span>
                </div>
              </div>
              <el-button
                type="primary"
                class="register-btn"
                @click.stop="handleRegister(event)"
                :disabled="!canRegister(event) || event.is_registered"
              >
                {{ getButtonText(event) }}
              </el-button>
            </div>
          </el-card>
        </el-col>
      </el-row>
      <el-empty v-else description="暂无赛事数据" />
    </div>

    <!-- 分页 -->
    <div class="pagination-wrapper" v-if="total > 0">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="[12, 24, 36, 48]"
        :total="total"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleSizeChange"
        @current-change="handlePageChange"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import { ElMessage } from 'element-plus'
import { Search, Calendar, Location, User, View, Clock } from '@element-plus/icons-vue'
import { getEventList } from '@/api/event'
import { formatDate } from '@/utils'

const router = useRouter()
const store = useStore()

const loading = ref(false)
const events = ref([])
const searchKeyword = ref('')
const filterStatus = ref('')
const orderBy = ref('-created_at')
const currentPage = ref(1)
const pageSize = ref(12)
const total = ref(0)
const defaultEventImage = 'https://via.placeholder.com/400x200?text=Event+Image'

// 获取登录状态
const isLogin = computed(() => store.getters['user/isLogin'])

// 获取赛事列表
const fetchEvents = async () => {
  loading.value = true
  try {
    const params = {
      status: 'published',
      page: currentPage.value,
      page_size: pageSize.value,
      ordering: orderBy.value
    }

    if (searchKeyword.value) {
      params.search = searchKeyword.value
    }

    if (filterStatus.value) {
      params.event_status = filterStatus.value
    }

    const data = await getEventList(params)
    events.value = data.results || []
    total.value = data.count || 0
  } catch (error) {
    console.error('获取赛事列表失败:', error)
    ElMessage.error('获取赛事列表失败')
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  currentPage.value = 1
  fetchEvents()
}

// 页码改变
const handlePageChange = (page) => {
  currentPage.value = page
  fetchEvents()
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

// 每页数量改变
const handleSizeChange = (size) => {
  pageSize.value = size
  currentPage.value = 1
  fetchEvents()
}

// 跳转到详情页
const goToDetail = (id) => {
  router.push(`/events/${id}`)
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

// 判断是否可以报名
const canRegister = (event) => {
  const now = new Date()
  const registrationStart = new Date(event.registration_start_time)
  const registrationEnd = new Date(event.registration_end_time)
  return now >= registrationStart && now <= registrationEnd
}

// 获取赛事状态类名
const getStatusClass = (event) => {
  const now = new Date()
  const registrationStart = new Date(event.registration_start_time)
  const registrationEnd = new Date(event.registration_end_time)
  const startTime = new Date(event.start_time)
  const endTime = new Date(event.end_time)

  if (now > endTime) {
    return 'status-finished'
  } else if (now >= startTime && now <= endTime) {
    return 'status-ongoing'
  } else if (now >= registrationStart && now <= registrationEnd) {
    return 'status-registration'
  } else if (now < registrationStart) {
    return 'status-waiting'
  } else {
    return 'status-closed'
  }
}

// 获取赛事状态文本
const getStatusText = (event) => {
  const now = new Date()
  const registrationStart = new Date(event.registration_start_time)
  const registrationEnd = new Date(event.registration_end_time)
  const startTime = new Date(event.start_time)
  const endTime = new Date(event.end_time)

  if (now > endTime) {
    return '已结束'
  } else if (now >= startTime && now <= endTime) {
    return '进行中'
  } else if (now >= registrationStart && now <= registrationEnd) {
    return '报名中'
  } else if (now < registrationStart) {
    return '即将开始'
  } else {
    return '报名截止'
  }
}

// 获取按钮文本
const getButtonText = (event) => {
  if (event.is_registered) {
    return '已报名'
  }
  if (!canRegister(event)) {
    return '报名已截止'
  }
  return '立即报名'
}

// 页面加载时获取数据
onMounted(() => {
  fetchEvents()
})
</script>

<style scoped>
.events-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

/* 筛选卡片 */
.filter-card {
  margin-bottom: 20px;
}

.filter-card :deep(.el-input),
.filter-card :deep(.el-select) {
  width: 100%;
}

/* 赛事列表 */
.events-list {
  min-height: 400px;
  margin-bottom: 20px;
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

.event-image-wrapper {
  position: relative;
  width: 100%;
  height: 200px;
  overflow: hidden;
}

.event-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}

.event-card:hover .event-image {
  transform: scale(1.1);
}

.event-status-badge {
  position: absolute;
  top: 10px;
  right: 10px;
  padding: 4px 12px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: bold;
  color: #fff;
  background-color: rgba(0, 0, 0, 0.5);
}

.status-registration {
  background-color: #67C23A !important;
}

.status-ongoing {
  background-color: #409EFF !important;
}

.status-finished {
  background-color: #909399 !important;
}

.status-waiting {
  background-color: #E6A23C !important;
}

.status-closed {
  background-color: #F56C6C !important;
}

.event-content {
  padding: 16px;
}

.event-title {
  margin: 0 0 12px 0;
  font-size: 18px;
  font-weight: 600;
  color: #303133;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.event-info {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 12px;
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

.event-stats {
  display: flex;
  justify-content: space-between;
  margin-bottom: 16px;
  padding: 10px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  color: #606266;
}

.stat-item .el-icon {
  color: #909399;
}

.register-btn {
  width: 100%;
}

/* 分页 */
.pagination-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 30px;
}

/* 响应式布局 */
@media screen and (max-width: 768px) {
  .events-page {
    padding: 10px;
  }

  .filter-card :deep(.el-col) {
    margin-bottom: 10px;
  }

  .event-image-wrapper {
    height: 180px;
  }

  .pagination-wrapper {
    overflow-x: auto;
  }

  .pagination-wrapper :deep(.el-pagination) {
    flex-wrap: wrap;
    justify-content: center;
  }
}

@media screen and (max-width: 576px) {
  .event-stats {
    flex-direction: column;
    gap: 6px;
  }

  .pagination-wrapper :deep(.el-pagination) {
    font-size: 12px;
  }
}
</style>
