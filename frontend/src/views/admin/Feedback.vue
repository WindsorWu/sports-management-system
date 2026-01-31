<template>
  <div class="feedback-page">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>反馈管理</span>
          <el-button type="primary" icon="Refresh" @click="fetchFeedbacks" :loading="loading">
            刷新
          </el-button>
        </div>
      </template>

      <!-- 搜索和筛选区域 -->
      <div class="search-bar">
        <el-input
          v-model="searchQuery"
          placeholder="搜索标题、用户名"
          clearable
          style="width: 300px; margin-right: 10px;"
          @clear="handleSearch"
          @keyup.enter="handleSearch"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
        <el-button type="primary" @click="handleSearch" :loading="loading">
          搜索
        </el-button>
        <el-select
          v-model="statusFilter"
          placeholder="筛选状态"
          clearable
          style="width: 150px; margin-left: 10px;"
          @change="handleSearch"
        >
          <el-option label="全部状态" value="" />
          <el-option label="待处理" value="pending" />
          <el-option label="处理中" value="processing" />
          <el-option label="已完成" value="completed" />
        </el-select>
      </div>

      <!-- 反馈列表表格 -->
      <el-table
        :data="feedbacks"
        v-loading="loading"
        stripe
        border
        style="width: 100%; margin-top: 20px;"
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column label="用户" width="150">
          <template #default="{ row }">
            {{ row.user_name || '-' }}
          </template>
        </el-table-column>
        <el-table-column prop="title" label="标题" min-width="200" show-overflow-tooltip />
        <el-table-column label="联系方式" width="150">
          <template #default="{ row }">
            {{ row.contact || '-' }}
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag v-if="row.status === 'pending'" type="warning">待处理</el-tag>
            <el-tag v-else-if="row.status === 'processing'" type="info">处理中</el-tag>
            <el-tag v-else-if="row.status === 'completed'" type="success">已完成</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="提交时间" width="180">
          <template #default="{ row }">
            {{ formatDateTime(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button
              type="primary"
              size="small"
              @click="handleViewDetail(row)"
            >
              查看详情
            </el-button>
            <el-button
              type="danger"
              size="small"
              @click="handleDelete(row)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handlePageChange"
        />
      </div>
    </el-card>

    <!-- 反馈详情对话框 -->
    <el-dialog
      v-model="detailDialogVisible"
      title="反馈详情"
      width="700px"
      @close="resetDetailForm"
    >
      <div v-if="currentFeedback" class="feedback-detail">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="反馈ID">
            {{ currentFeedback.id }}
          </el-descriptions-item>
          <el-descriptions-item label="用户">
            {{ currentFeedback.user_name || '-' }}
          </el-descriptions-item>
          <el-descriptions-item label="联系方式" :span="2">
            {{ currentFeedback.contact || '-' }}
          </el-descriptions-item>
          <el-descriptions-item label="反馈标题" :span="2">
            {{ currentFeedback.title }}
          </el-descriptions-item>
          <el-descriptions-item label="反馈内容" :span="2">
            <div class="feedback-content">{{ currentFeedback.content }}</div>
          </el-descriptions-item>
          <el-descriptions-item label="提交时间" :span="2">
            {{ formatDateTime(currentFeedback.created_at) }}
          </el-descriptions-item>
          <el-descriptions-item label="当前状态" :span="2">
            <el-tag v-if="currentFeedback.status === 'pending'" type="warning">待处理</el-tag>
            <el-tag v-else-if="currentFeedback.status === 'processing'" type="info">处理中</el-tag>
            <el-tag v-else-if="currentFeedback.status === 'completed'" type="success">已完成</el-tag>
          </el-descriptions-item>
        </el-descriptions>

        <el-divider />

        <div class="reply-section">
          <h4>管理员回复</h4>
          <div v-if="currentFeedback.reply" class="reply-content">
            <p><strong>回复内容：</strong></p>
            <p>{{ currentFeedback.reply }}</p>
            <p class="reply-time">回复时间：{{ formatDateTime(currentFeedback.reply_at) }}</p>
          </div>
          <el-empty v-else description="暂无回复" :image-size="80" />

          <el-form
            ref="replyFormRef"
            :model="replyForm"
            :rules="replyFormRules"
            label-width="100px"
            style="margin-top: 20px;"
          >
            <el-form-item label="回复内容" prop="reply">
              <el-input
                v-model="replyForm.reply"
                type="textarea"
                :rows="4"
                placeholder="请输入回复内容"
              />
            </el-form-item>

            <el-form-item label="更新状态" prop="status">
              <el-select v-model="replyForm.status" placeholder="请选择状态" style="width: 100%;">
                <el-option label="待处理" value="pending" />
                <el-option label="处理中" value="processing" />
                <el-option label="已完成" value="completed" />
              </el-select>
            </el-form-item>
          </el-form>
        </div>
      </div>

      <template #footer>
        <el-button @click="detailDialogVisible = false">关闭</el-button>
        <el-button type="primary" @click="handleSubmitReply" :loading="replySubmitting">
          提交回复
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search } from '@element-plus/icons-vue'
import { getFeedbackList, getFeedbackDetail, replyFeedback, updateFeedbackStatus, deleteFeedback } from '@/api/feedback'

// 搜索和筛选
const searchQuery = ref('')
const statusFilter = ref('')

// 反馈列表
const feedbacks = ref([])
const loading = ref(false)

// 分页
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

// 详情对话框
const detailDialogVisible = ref(false)
const currentFeedback = ref(null)
const replySubmitting = ref(false)
const replyFormRef = ref(null)

// 回复表单
const replyForm = reactive({
  reply: '',
  status: 'processing'
})

// 回复表单验证规则
const replyFormRules = {
  reply: [
    { required: true, message: '请输入回复内容', trigger: 'blur' }
  ],
  status: [
    { required: true, message: '请选择状态', trigger: 'change' }
  ]
}

// 获取反馈列表
const fetchFeedbacks = async () => {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize.value
    }

    if (searchQuery.value) {
      params.search = searchQuery.value
    }

    if (statusFilter.value) {
      params.status = statusFilter.value
    }

    const response = await getFeedbackList(params)
    feedbacks.value = response.results || []
    total.value = response.count || 0
  } catch (error) {
    console.error('获取反馈列表失败:', error)
    ElMessage.error('获取反馈列表失败')
  } finally {
    loading.value = false
  }
}

// 搜索处理
const handleSearch = () => {
  currentPage.value = 1
  fetchFeedbacks()
}

// 分页大小变化
const handleSizeChange = (newSize) => {
  pageSize.value = newSize
  currentPage.value = 1
  fetchFeedbacks()
}

// 页码变化
const handlePageChange = (newPage) => {
  currentPage.value = newPage
  fetchFeedbacks()
}

// 查看详情
const handleViewDetail = async (feedback) => {
  try {
    const response = await getFeedbackDetail(feedback.id)
    currentFeedback.value = response

    // 初始化回复表单
    replyForm.reply = response.reply || ''
    replyForm.status = response.status

    detailDialogVisible.value = true
  } catch (error) {
    console.error('获取反馈详情失败:', error)
    ElMessage.error('获取反馈详情失败')
  }
}

// 提交回复
const handleSubmitReply = async () => {
  try {
    await replyFormRef.value.validate()

    replySubmitting.value = true

    await replyFeedback(currentFeedback.value.id, replyForm.reply)

    // 如果状态有变化，也更新状态
    if (replyForm.status !== currentFeedback.value.status) {
      await updateFeedbackStatus(currentFeedback.value.id, replyForm.status)
    }

    ElMessage.success('回复成功')
    detailDialogVisible.value = false
    await fetchFeedbacks()
  } catch (error) {
    if (error.message) {
      console.error('回复失败:', error)
      ElMessage.error(error.response?.data?.detail || error.response?.data?.error || '回复失败')
    }
  } finally {
    replySubmitting.value = false
  }
}

// 删除反馈
const handleDelete = async (feedback) => {
  try {
    await ElMessageBox.confirm(
      `确认删除该反馈吗？此操作不可恢复！`,
      '删除确认',
      {
        confirmButtonText: '确认删除',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'el-button--danger'
      }
    )

    await deleteFeedback(feedback.id)
    ElMessage.success('反馈删除成功')
    await fetchFeedbacks()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除反馈失败:', error)
      ElMessage.error(error.response?.data?.detail || error.response?.data?.error || '删除反馈失败')
    }
  }
}

// 重置详情表单
const resetDetailForm = () => {
  currentFeedback.value = null
  replyForm.reply = ''
  replyForm.status = 'processing'
  replyFormRef.value?.clearValidate()
}

// 格式化日期时间
const formatDateTime = (dateStr) => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(() => {
  fetchFeedbacks()
})
</script>

<style scoped>
.feedback-page {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: bold;
}

.search-bar {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.feedback-detail {
  padding: 10px 0;
}

.feedback-content {
  white-space: pre-wrap;
  word-break: break-word;
  line-height: 1.6;
  max-height: 200px;
  overflow-y: auto;
}

.reply-section {
  margin-top: 20px;
}

.reply-section h4 {
  margin-bottom: 15px;
  font-size: 16px;
  font-weight: bold;
}

.reply-content {
  padding: 15px;
  background-color: #f5f7fa;
  border-radius: 4px;
  margin-bottom: 15px;
}

.reply-content p {
  margin: 8px 0;
  line-height: 1.6;
}

.reply-time {
  color: #909399;
  font-size: 12px;
  margin-top: 10px;
}

@media (max-width: 768px) {
  .feedback-page {
    padding: 10px;
  }

  .search-bar {
    flex-direction: column;
    align-items: stretch;
  }

  .search-bar .el-input,
  .search-bar .el-select {
    width: 100% !important;
    margin-left: 0 !important;
  }

  .card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
}
</style>
