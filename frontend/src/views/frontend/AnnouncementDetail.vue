<template>
  <div class="announcement-detail-page">
    <el-card v-loading="loading" shadow="hover" class="detail-card">
      <!-- 返回按钮 -->
      <div class="back-button">
        <el-button @click="goBack">
          <el-icon><ArrowLeft /></el-icon> 返回列表
        </el-button>
      </div>

      <div v-if="announcement.id" class="detail-content">
        <!-- 标题 -->
        <h1 class="announcement-title">
          {{ announcement.title }}
        </h1>

        <!-- 元信息 -->
        <div class="announcement-meta">
          <span class="meta-item">
            <el-icon><Calendar /></el-icon>
            发布时间：{{ formatDate(announcement.published_at || announcement.created_at, 'YYYY-MM-DD HH:mm') }}
          </span>
          <span class="meta-item">
            <el-icon><View /></el-icon>
            浏览量：{{ announcement.view_count || 0 }}
          </span>
          <span v-if="announcement.author_name" class="meta-item">
            <el-icon><User /></el-icon>
            发布人：{{ announcement.author_name }}
          </span>
        </div>

        <el-divider />

        <!-- 封面图片 -->
        <div v-if="announcement.image" class="announcement-image">
          <img
            :src="announcement.image"
            :alt="announcement.title"
            @error="handleImageError"
          />
        </div>

        <!-- 公告内容 -->
        <div class="announcement-content" v-html="announcement.content"></div>

        <!-- 底部分隔 -->
        <el-divider />

        <!-- 底部操作 -->
        <div class="announcement-footer">
          <el-button type="primary" @click="goBack">
            <el-icon><ArrowLeft /></el-icon> 返回列表
          </el-button>
        </div>
      </div>

      <!-- 加载失败提示 -->
      <el-empty v-else-if="!loading" description="公告不存在或已被删除">
        <el-button type="primary" @click="goBack">返回列表</el-button>
      </el-empty>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { ArrowLeft, Calendar, View, User } from '@element-plus/icons-vue'
import { getAnnouncementDetail } from '@/api/announcement'
import { formatDate } from '@/utils'

const router = useRouter()
const route = useRoute()

// 加载状态
const loading = ref(false)

// 公告详情
const announcement = ref({})

// 加载公告详情
const loadAnnouncementDetail = async () => {
  loading.value = true
  try {
    const id = route.params.id
    if (!id) {
      ElMessage.error('公告ID不存在')
      goBack()
      return
    }

    const data = await getAnnouncementDetail(id)
    announcement.value = data
  } catch (error) {
    ElMessage.error(error.message || '加载公告详情失败')
    announcement.value = {}
  } finally {
    loading.value = false
  }
}

// 返回列表
const goBack = () => {
  router.push('/announcements')
}

// 图片加载失败处理
const handleImageError = (e) => {
  e.target.style.display = 'none'
}

// 初始化
onMounted(() => {
  loadAnnouncementDetail()
})
</script>

<style scoped>
.announcement-detail-page {
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
}

.detail-card {
  border-radius: 8px;
  min-height: 400px;
}

/* 返回按钮 */
.back-button {
  margin-bottom: 20px;
}

/* 详情内容 */
.detail-content {
  animation: fadeIn 0.3s ease-in;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 标题 */
.announcement-title {
  margin: 0 0 20px 0;
  font-size: 28px;
  font-weight: 600;
  color: #303133;
  line-height: 1.4;
  text-align: center;
}

/* 元信息 */
.announcement-meta {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 24px;
  flex-wrap: wrap;
  margin-bottom: 20px;
}

.meta-item {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  color: #909399;
}

.meta-item .el-icon {
  font-size: 16px;
}

/* 封面图片 */
.announcement-image {
  margin: 20px 0;
  text-align: center;
}

.announcement-image img {
  max-width: 100%;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* 公告内容 */
.announcement-content {
  font-size: 16px;
  line-height: 1.8;
  color: #303133;
  margin: 30px 0;
  word-wrap: break-word;
  word-break: break-word;
}

/* 富文本内容样式 */
.announcement-content :deep(h1),
.announcement-content :deep(h2),
.announcement-content :deep(h3),
.announcement-content :deep(h4),
.announcement-content :deep(h5),
.announcement-content :deep(h6) {
  margin: 20px 0 12px 0;
  font-weight: 600;
  color: #303133;
}

.announcement-content :deep(h1) {
  font-size: 24px;
}

.announcement-content :deep(h2) {
  font-size: 22px;
}

.announcement-content :deep(h3) {
  font-size: 20px;
}

.announcement-content :deep(p) {
  margin: 12px 0;
}

.announcement-content :deep(img) {
  max-width: 100%;
  height: auto;
  border-radius: 4px;
  margin: 16px 0;
}

.announcement-content :deep(ul),
.announcement-content :deep(ol) {
  margin: 12px 0;
  padding-left: 24px;
}

.announcement-content :deep(li) {
  margin: 8px 0;
}

.announcement-content :deep(blockquote) {
  margin: 16px 0;
  padding: 12px 16px;
  background-color: #f5f7fa;
  border-left: 4px solid #409eff;
  color: #606266;
}

.announcement-content :deep(code) {
  padding: 2px 6px;
  background-color: #f5f7fa;
  border-radius: 3px;
  font-family: 'Courier New', monospace;
  font-size: 14px;
  color: #e83e8c;
}

.announcement-content :deep(pre) {
  margin: 16px 0;
  padding: 16px;
  background-color: #282c34;
  border-radius: 4px;
  overflow-x: auto;
}

.announcement-content :deep(pre code) {
  padding: 0;
  background-color: transparent;
  color: #abb2bf;
}

.announcement-content :deep(table) {
  width: 100%;
  border-collapse: collapse;
  margin: 16px 0;
}

.announcement-content :deep(table th),
.announcement-content :deep(table td) {
  padding: 8px 12px;
  border: 1px solid #dcdfe6;
  text-align: left;
}

.announcement-content :deep(table th) {
  background-color: #f5f7fa;
  font-weight: 600;
}

.announcement-content :deep(a) {
  color: #409eff;
  text-decoration: none;
}

.announcement-content :deep(a:hover) {
  text-decoration: underline;
}

/* 底部操作 */
.announcement-footer {
  text-align: center;
  margin-top: 20px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .announcement-detail-page {
    padding: 16px;
  }

  .announcement-title {
    font-size: 22px;
  }

  .announcement-meta {
    flex-direction: column;
    gap: 8px;
  }

  .announcement-content {
    font-size: 15px;
  }

  .announcement-content :deep(h1) {
    font-size: 20px;
  }

  .announcement-content :deep(h2) {
    font-size: 18px;
  }

  .announcement-content :deep(h3) {
    font-size: 17px;
  }

  .announcement-content :deep(pre) {
    padding: 12px;
    font-size: 13px;
  }

  .announcement-content :deep(table) {
    display: block;
    overflow-x: auto;
  }
}

/* 打印样式 */
@media print {
  .back-button,
  .announcement-footer {
    display: none;
  }

  .announcement-detail-page {
    padding: 0;
  }

  .detail-card {
    box-shadow: none;
    border: none;
  }
}
</style>
