<template>
  <div class="comment-page">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>评论管理</span>
          <el-button type="primary" icon="Refresh" @click="fetchComments" :loading="loading">
            刷新
          </el-button>
        </div>
      </template>

      <div class="search-bar">
        <el-input
          v-model="searchQuery"
          placeholder="搜索用户名、赛事名称或评论内容"
          clearable
          style="width: 320px;"
          @clear="handleSearch"
          @keyup.enter="handleSearch"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
        <el-select
          v-model="approvalFilter"
          placeholder="筛选审核状态"
          clearable
          style="width: 180px;"
          @change="handleSearch"
        >
          <el-option label="全部状态" value="" />
          <el-option label="已通过" value="approved" />
          <el-option label="待审核" value="pending" />
        </el-select>
        <el-button type="primary" @click="handleSearch" :loading="loading">搜索</el-button>
      </div>

      <el-table
        :data="comments"
        v-loading="loading"
        stripe
        border
        style="width: 100%; margin-top: 20px;"
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column label="用户" width="160">
          <template #default="{ row }">
            {{ row.user_name || row.user_username || '匿名' }}
          </template>
        </el-table-column>
        <el-table-column label="赛事" width="220">
          <template #default="{ row }">
            {{ row.event_title || '未知赛事' }}
          </template>
        </el-table-column>
        <el-table-column label="评论内容">
          <template #default="{ row }">
            <div class="comment-content">
              {{ row.content }}
            </div>
          </template>
        </el-table-column>
        <el-table-column label="审核状态" width="140">
          <template #default="{ row }">
            <el-tag v-if="row.is_approved" type="success">已通过</el-tag>
            <el-tag v-else type="danger">待审核</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="提交时间" width="180">
          <template #default="{ row }">
            {{ formatDateTime(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="220" fixed="right">
          <template #default="{ row }">
            <el-button
              v-if="!row.is_approved"
              type="success"
              size="mini"
              @click="handleApprove(row)"
            >
              通过
            </el-button>
            <el-button
              v-if="row.is_approved"
              type="warning"
              size="mini"
              @click="handleReject(row)"
            >
              驳回
            </el-button>
            <el-button type="danger" size="mini" @click="handleDelete(row)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

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
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search } from '@element-plus/icons-vue'
import {
  getCommentList,
  approveComment,
  rejectComment,
  deleteComment
} from '@/api/interaction'

const comments = ref([])
const loading = ref(false)
const searchQuery = ref('')
const approvalFilter = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

const fetchComments = async () => {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize.value,
      target_type: 'events.event'
    }
    if (searchQuery.value) {
      params.search = searchQuery.value
    }
    if (approvalFilter.value) {
      params.is_approved = approvalFilter.value === 'approved'
    }

    const response = await getCommentList(params)
    comments.value = response.results || []
    total.value = response.count || 0
  } catch (error) {
    console.error('获取评论列表失败:', error)
    ElMessage.error('获取评论列表失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  currentPage.value = 1
  fetchComments()
}

const handleSizeChange = (newSize) => {
  pageSize.value = newSize
  currentPage.value = 1
  fetchComments()
}

const handlePageChange = (newPage) => {
  currentPage.value = newPage
  fetchComments()
}

const handleApprove = async (comment) => {
  try {
    await approveComment(comment.id)
    ElMessage.success('评论已通过审核')
    fetchComments()
  } catch (error) {
    console.error('审核通过失败:', error)
    ElMessage.error(error.response?.data?.detail || '审核通过失败')
  }
}

const handleReject = async (comment) => {
  try {
    await rejectComment(comment.id)
    ElMessage.success('评论已被驳回')
    fetchComments()
  } catch (error) {
    console.error('驳回失败:', error)
    ElMessage.error(error.response?.data?.detail || '驳回失败')
  }
}

const handleDelete = async (comment) => {
  try {
    await ElMessageBox.confirm('确认删除该评论？此操作不可恢复', '删除确认', {
      confirmButtonText: '确认删除',
      cancelButtonText: '取消',
      type: 'warning',
      confirmButtonClass: 'el-button--danger'
    })

    await deleteComment(comment.id)
    ElMessage.success('评论删除成功')
    fetchComments()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除评论失败:', error)
      ElMessage.error(error.response?.data?.detail || '删除失败')
    }
  }
}

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
  fetchComments()
})
</script>

<style scoped>
.comment-page {
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

.comment-content {
  white-space: pre-wrap;
  word-break: break-word;
  max-height: 160px;
  overflow: hidden;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

@media (max-width: 768px) {
  .search-bar {
    flex-direction: column;
    align-items: stretch;
  }

  .search-bar .el-input,
  .search-bar .el-select {
    width: 100% !important;
  }
}
</style>
