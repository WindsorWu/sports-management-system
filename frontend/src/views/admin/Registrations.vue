<template>
  <div class="registrations-page">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>报名管理</span>
          <div>
            <el-button type="primary" icon="Refresh" @click="fetchRegistrations" :loading="loading">
              刷新
            </el-button>
            <el-button type="success" icon="Download" @click="handleExport" :loading="exporting" :disabled="!eventFilter">
              导出Excel
            </el-button>
          </div>
        </div>
      </template>

      <!-- 搜索和筛选区域 -->
      <div class="search-bar">
        <el-input
          v-model="searchQuery"
          placeholder="搜索用户名、赛事名"
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
          v-model="eventFilter"
          placeholder="请选择赛事"
          style="width: 240px; margin-left: 10px;"
          filterable
          :disabled="eventList.length === 0"
          @change="handleSearch"
        >
          <el-option
            v-for="event in eventList"
            :key="event.id"
            :label="event.title"
            :value="event.id"
          />
        </el-select>
        <el-select
          v-model="statusFilter"
          placeholder="报名状态"
          clearable
          style="width: 150px; margin-left: 10px;"
          @change="handleSearch"
        >
          <el-option label="全部" value="" />
          <el-option label="待审核" value="pending">
            <el-badge :value="pendingCount" :max="99" class="status-badge">
              <span>待审核</span>
            </el-badge>
          </el-option>
          <el-option label="已通过" value="approved" />
          <el-option label="已拒绝" value="rejected" />
        </el-select>
      </div>

      <!-- 报名列表表格 -->
      <el-table
        :data="registrations"
        v-loading="loading"
        stripe
        style="width: 100%; margin-top: 20px;"
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="registration_number" label="报名编号" width="200" show-overflow-tooltip />
        <el-table-column label="赛事名称" min-width="180" show-overflow-tooltip>
          <template #default="{ row }">
            {{ row.event_title || '-' }}
          </template>
        </el-table-column>
        <el-table-column label="参赛者姓名" width="120">
          <template #default="{ row }">
            {{ row.participant_name || '-' }}
          </template>
        </el-table-column>
        <el-table-column label="联系电话" width="130">
          <template #default="{ row }">
            {{ row.participant_phone || '-' }}
          </template>
        </el-table-column>
        <el-table-column label="报名用户" width="120">
          <template #default="{ row }">
            {{ row.user_username || '-' }}
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="报名时间" width="180">
          <template #default="{ row }">
            {{ formatDateTime(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag v-if="row.status === 'pending'" type="warning">待审核</el-tag>
            <el-tag v-else-if="row.status === 'approved'" type="success">已通过</el-tag>
            <el-tag v-else-if="row.status === 'rejected'" type="danger">已拒绝</el-tag>
            <el-tag v-else-if="row.status === 'cancelled'" type="info">已取消</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="备注" min-width="120" show-overflow-tooltip>
          <template #default="{ row }">
            {{ row.remarks || '-' }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="250" fixed="right">
          <template #default="{ row }">
            <el-button
              type="primary"
              size="small"
              @click="handleViewDetail(row)"
            >
              详情
            </el-button>
            <el-button
              v-if="row.status === 'pending'"
              type="success"
              size="small"
              @click="handleApprove(row)"
              :loading="row.approving"
            >
              通过
            </el-button>
            <el-button
              v-if="row.status === 'pending'"
              type="danger"
              size="small"
              @click="handleReject(row)"
              :loading="row.rejecting"
            >
              拒绝
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

    <!-- 报名详情对话框 -->
    <el-dialog
      v-model="detailDialogVisible"
      title="报名详情"
      width="700px"
    >
      <el-descriptions v-if="currentRegistration" :column="2" border>
        <el-descriptions-item label="报名编号" :span="2">
          {{ currentRegistration.registration_number || '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="报名状态" :span="2">
          <el-tag v-if="currentRegistration.status === 'pending'" type="warning">待审核</el-tag>
          <el-tag v-else-if="currentRegistration.status === 'approved'" type="success">已通过</el-tag>
          <el-tag v-else-if="currentRegistration.status === 'rejected'" type="danger">已拒绝</el-tag>
          <el-tag v-else-if="currentRegistration.status === 'cancelled'" type="info">已取消</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="赛事名称" :span="2">
          {{ currentRegistration.event_title || '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="参赛者姓名">
          {{ currentRegistration.participant_name || '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="参赛者电话">
          {{ currentRegistration.participant_phone || '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="身份证号" :span="2">
          {{ currentRegistration.participant_id_card || '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="性别">
          {{ currentRegistration.participant_gender === 'M' ? '男' : currentRegistration.participant_gender === 'F' ? '女' : '其他' }}
        </el-descriptions-item>
        <el-descriptions-item label="出生日期">
          {{ currentRegistration.participant_birth_date || '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="所属单位" :span="2">
          {{ currentRegistration.participant_organization || '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="紧急联系人">
          {{ currentRegistration.emergency_contact || '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="紧急联系电话">
          {{ currentRegistration.emergency_phone || '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="报名用户">
          {{ currentRegistration.user_username || '-' }}
        </el-descriptions-item>
        <el-descriptions-item label="报名时间">
          {{ formatDateTime(currentRegistration.created_at) }}
        </el-descriptions-item>
        <el-descriptions-item v-if="currentRegistration.reviewed_by_name" label="审核人">
          {{ currentRegistration.reviewed_by_name }}
        </el-descriptions-item>
        <el-descriptions-item v-if="currentRegistration.reviewed_at" label="审核时间">
          {{ formatDateTime(currentRegistration.reviewed_at) }}
        </el-descriptions-item>
        <el-descriptions-item v-if="currentRegistration.remarks" label="报名备注" :span="2">
          {{ currentRegistration.remarks }}
        </el-descriptions-item>
        <el-descriptions-item v-if="currentRegistration.review_remarks" label="审核备注" :span="2">
          {{ currentRegistration.review_remarks }}
        </el-descriptions-item>
      </el-descriptions>

      <template #footer>
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <div>
            <el-button
              v-if="currentRegistration?.status === 'pending'"
              type="success"
              @click="handleApprove(currentRegistration)"
              :loading="currentRegistration?.approving"
            >
              通过审核
            </el-button>
            <el-button
              v-if="currentRegistration?.status === 'pending'"
              type="danger"
              @click="handleReject(currentRegistration)"
              :loading="currentRegistration?.rejecting"
            >
              拒绝审核
            </el-button>
          </div>
          <el-button @click="detailDialogVisible = false">关闭</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search } from '@element-plus/icons-vue'
import { getRegistrationList, getRegistrationDetail, approveRegistration, rejectRegistration, exportRegistrations } from '@/api/registration'
import { getEventList } from '@/api/event'

const route = useRoute()

// 搜索和筛选
const searchQuery = ref('')
const statusFilter = ref('')
const eventFilter = ref('')
const pendingCount = ref(0)

// 报名列表
const registrations = ref([])
const loading = ref(false)

// 分页
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

// 详情对话框
const detailDialogVisible = ref(false)
const currentRegistration = ref(null)

// 导出状态
const exporting = ref(false)

// 赛事列表
const eventList = ref([])

// 获取报名列表
const fetchRegistrations = async () => {
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

    if (eventFilter.value) {
      params.event = eventFilter.value
    }

    const response = await getRegistrationList(params)
    registrations.value = response.results || []
    total.value = response.count || 0

    // 获取待审核数量
    if (!statusFilter.value || statusFilter.value === 'pending') {
      const pendingResponse = await getRegistrationList({ status: 'pending', page_size: 1 })
      pendingCount.value = pendingResponse.count || 0
    }
  } catch (error) {
    console.error('获取报名列表失败:', error)
    ElMessage.error('获取报名列表失败')
  } finally {
    loading.value = false
  }
}

// 获取赛事列表
const fetchEvents = async () => {
  try {
    const response = await getEventList({ page_size: 1000 })
    eventList.value = response.results || []
    if (eventList.value.length === 0) {
      ElMessage.warning('暂无赛事可供筛选，无法导出')
    }
  } catch (error) {
    console.error('获取赛事列表失败:', error)
  }
}

// 搜索处理
const handleSearch = () => {
  currentPage.value = 1
  fetchRegistrations()
}

// 分页大小变化
const handleSizeChange = (newSize) => {
  pageSize.value = newSize
  currentPage.value = 1
  fetchRegistrations()
}

// 页码变化
const handlePageChange = (newPage) => {
  currentPage.value = newPage
  fetchRegistrations()
}

// 查看详情
const handleViewDetail = async (registration) => {
  try {
    const response = await getRegistrationDetail(registration.id)
    currentRegistration.value = response
    detailDialogVisible.value = true
  } catch (error) {
    console.error('获取报名详情失败:', error)
    ElMessage.error('获取报名详情失败')
  }
}

// 审核通过
const handleApprove = async (row) => {
  try {
    const { value: review_remarks } = await ElMessageBox.prompt('请输入审核备注（可选）', '通过审核', {
      confirmButtonText: '确认',
      cancelButtonText: '取消',
      inputType: 'textarea'
    })

    row.approving = true
    await approveRegistration(row.id, review_remarks || '')
    ElMessage.success('审核通过')

    // 关闭详情对话框（如果打开）
    if (detailDialogVisible.value) {
      detailDialogVisible.value = false
    }

    await fetchRegistrations()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('审核失败:', error)
      ElMessage.error(error.response?.data?.error || '审核失败')
    }
  } finally {
    row.approving = false
  }
}

// 审核拒绝
const handleReject = async (row) => {
  try {
    const { value: review_remarks } = await ElMessageBox.prompt('请输入拒绝原因', '拒绝审核', {
      confirmButtonText: '确认',
      cancelButtonText: '取消',
      inputPattern: /.+/,
      inputErrorMessage: '请输入拒绝原因',
      inputType: 'textarea'
    })

    row.rejecting = true
    await rejectRegistration(row.id, review_remarks)
    ElMessage.success('已拒绝')

    // 关闭详情对话框（如果打开）
    if (detailDialogVisible.value) {
      detailDialogVisible.value = false
    }

    await fetchRegistrations()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('拒绝失败:', error)
      ElMessage.error(error.response?.data?.error || '拒绝失败')
    }
  } finally {
    row.rejecting = false
  }
}

// 导出Excel
const handleExport = async () => {
  if (!eventFilter.value) {
    ElMessage.warning('请先选择一个赛事再导出')
    return
  }
  exporting.value = true
  try {
    const params = {}

    if (searchQuery.value) {
      params.search = searchQuery.value
    }

    if (statusFilter.value) {
      params.status = statusFilter.value
    }

    params.event = eventFilter.value

    const response = await exportRegistrations(params)

    // 创建下载链接
    const url = window.URL.createObjectURL(new Blob([response]))
    const link = document.createElement('a')
    link.href = url

    // 使用默认文件名
    let fileName = '报名数据.xlsx'

    link.setAttribute('download', fileName)
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)

    ElMessage.success('导出成功')
  } catch (error) {
    console.error('导出失败:', error)
    ElMessage.error('导出失败')
  } finally {
    exporting.value = false
  }
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
  // 从URL参数读取状态筛选
  if (route.query.status) {
    statusFilter.value = route.query.status
  }

  fetchEvents()
  fetchRegistrations()
})
</script>

<style scoped>
.registrations-page {
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

.status-badge {
  width: 100%;
  display: inline-block;
}

@media (max-width: 768px) {
  .registrations-page {
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
}
</style>
