<template>
  <div class="announcements-page">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1 class="page-title">系统公告</h1>
      <p class="page-description">及时了解最新的赛事动态和系统通知</p>
    </div>

    <!-- 搜索框 -->
    <el-card class="search-card" shadow="hover">
      <el-form :inline="true" :model="searchForm" @submit.prevent="handleSearch">
        <el-form-item>
          <el-input
            v-model="searchForm.search"
            placeholder="搜索公告标题"
            clearable
            @clear="handleSearch"
            style="width: 300px"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">
            <el-icon><Search /></el-icon> 搜索
          </el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 公告列表 -->
    <div v-loading="loading" class="announcements-list">
      <div v-if="announcements.length === 0 && !loading" class="empty-container">
        <el-empty description="暂无公告" />
      </div>

      <el-card
        v-for="announcement in announcements"
        :key="announcement.id"
        class="announcement-card"
        shadow="hover"
        @click="goToDetail(announcement.id)"
      >
        <div class="announcement-content">
          <div v-if="announcement.image" class="announcement-image">
            <img
              :src="announcement.image"
              :alt="announcement.title"
              @error="handleImageError"
            />
          </div>
          <div class="announcement-info">
            <h2 class="announcement-title">
              <el-icon class="title-icon"><Bell /></el-icon>
              {{ announcement.title }}
            </h2>
            <p class="announcement-summary">
              {{ announcement.summary || (announcement.content ? announcement.content.substring(0, 150) + '...' : '暂无简介') }}
            </p>
            <div class="announcement-meta">
              <div class="meta-left">
                <span class="meta-item">
                  <el-icon><Calendar /></el-icon>
                  {{ formatDate(announcement.published_at || announcement.created_at, 'YYYY-MM-DD HH:mm') }}
                </span>
                <span class="meta-item">
                  <el-icon><View /></el-icon>
                  浏览 {{ announcement.view_count || 0 }} 次
                </span>
              </div>
              <el-button type="primary" link>
                查看详情 <el-icon><ArrowRight /></el-icon>
              </el-button>
            </div>
          </div>
        </div>
      </el-card>
    </div>

    <!-- 分页 -->
    <div v-if="total > 0" class="pagination-container">
      <el-pagination
        v-model:current-page="pagination.page"
        v-model:page-size="pagination.page_size"
        :total="total"
        :page-sizes="[10, 20, 30, 50]"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleSizeChange"
        @current-change="handlePageChange"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Search, Calendar, View, Bell, ArrowRight } from '@element-plus/icons-vue'
import { getAnnouncementList } from '@/api/announcement'
import { formatDate } from '@/utils'

const router = useRouter()

// 加载状态
const loading = ref(false)

// 搜索表单
const searchForm = reactive({
  search: ''
})

// 分页信息
const pagination = reactive({
  page: 1,
  page_size: 10
})

// 数据
const announcements = ref([])
const total = ref(0)

// 加载公告列表
const loadAnnouncements = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.page_size
    }

    if (searchForm.search) {
      params.search = searchForm.search
    }

    const data = await getAnnouncementList(params)

    // 处理分页数据
    if (data.results) {
      announcements.value = data.results
      total.value = data.count
    } else {
      // 如果后端没有分页，直接返回数组
      announcements.value = data
      total.value = data.length
    }
  } catch (error) {
    ElMessage.error(error.message || '加载公告列表失败')
    announcements.value = []
    total.value = 0
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  pagination.page = 1
  loadAnnouncements()
}

// 重置
const handleReset = () => {
  searchForm.search = ''
  pagination.page = 1
  loadAnnouncements()
}

// 页码改变
const handlePageChange = (page) => {
  pagination.page = page
  loadAnnouncements()
  // 滚动到顶部
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

// 每页数量改变
const handleSizeChange = (size) => {
  pagination.page_size = size
  pagination.page = 1
  loadAnnouncements()
}

// 跳转到详情页
const goToDetail = (id) => {
  router.push(`/announcements/${id}`)
}

// 图片加载失败处理
const handleImageError = (e) => {
  e.target.style.display = 'none'
}

// 初始化
onMounted(() => {
  loadAnnouncements()
})
</script>

<style scoped>
.announcements-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

/* 页面头部 */
.page-header {
  text-align: center;
  margin-bottom: 30px;
}

.page-title {
  margin: 0 0 12px 0;
  font-size: 32px;
  font-weight: 600;
  color: #303133;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.page-description {
  margin: 0;
  font-size: 16px;
  color: #909399;
}

/* 搜索卡片 */
.search-card {
  margin-bottom: 20px;
  border-radius: 8px;
}

.search-card :deep(.el-card__body) {
  padding: 16px 20px;
}

.search-card .el-form {
  margin: 0;
}

.search-card .el-form-item {
  margin-bottom: 0;
}

/* 公告列表 */
.announcements-list {
  min-height: 400px;
}

.announcement-card {
  margin-bottom: 20px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.announcement-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.announcement-card:last-child {
  margin-bottom: 0;
}

.announcement-content {
  display: flex;
  gap: 20px;
}

/* 公告图片 */
.announcement-image {
  flex-shrink: 0;
  width: 200px;
  height: 140px;
  border-radius: 8px;
  overflow: hidden;
  background-color: #f5f7fa;
}

.announcement-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}

.announcement-card:hover .announcement-image img {
  transform: scale(1.05);
}

/* 公告信息 */
.announcement-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.announcement-title {
  margin: 0 0 12px 0;
  font-size: 20px;
  font-weight: 600;
  color: #303133;
  display: flex;
  align-items: center;
  gap: 8px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.title-icon {
  color: #409eff;
  font-size: 22px;
}

.announcement-summary {
  margin: 0 0 auto 0;
  font-size: 14px;
  line-height: 1.6;
  color: #606266;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

.announcement-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 16px;
  padding-top: 12px;
  border-top: 1px solid #f0f0f0;
}

.meta-left {
  display: flex;
  gap: 20px;
}

.meta-item {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  color: #909399;
}

.meta-item .el-icon {
  font-size: 14px;
}

/* 空状态 */
.empty-container {
  padding: 60px 0;
}

/* 分页 */
.pagination-container {
  display: flex;
  justify-content: center;
  margin-top: 30px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .announcements-page {
    padding: 16px;
  }

  .page-title {
    font-size: 24px;
  }

  .page-description {
    font-size: 14px;
  }

  .search-card .el-form {
    display: block;
  }

  .search-card .el-form-item {
    margin-bottom: 12px;
    display: block;
  }

  .search-card .el-input {
    width: 100% !important;
  }

  .announcement-content {
    flex-direction: column;
  }

  .announcement-image {
    width: 100%;
    height: 200px;
  }

  .announcement-title {
    font-size: 18px;
  }

  .announcement-meta {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .meta-left {
    flex-direction: column;
    gap: 8px;
  }

  .pagination-container :deep(.el-pagination) {
    flex-wrap: wrap;
    justify-content: center;
  }
}
</style>
