<template>
  <div class="results-page">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>成绩管理</span>
          <div>
            <el-button type="primary" icon="Refresh" @click="fetchResults" :loading="loading">
              刷新
            </el-button>
            <el-button
              type="success"
              @click="handleBulkPublish"
              :disabled="!eventFilter || !hasSelection"
            >
              批量公开成绩
            </el-button>
            <el-button
              type="danger"
              @click="handleBulkDelete"
              :disabled="!eventFilter || !hasSelection"
            >
              批量删除成绩
            </el-button>
            <el-button
              type="info"
              icon="Upload"
              @click="handleImportOpen"
              :disabled="!eventFilter"
            >
              批量导入成绩
            </el-button>
            <el-button type="success" icon="Plus" @click="handleAdd">
              录入成绩
            </el-button>
            <el-button type="warning" icon="Download" @click="handleExport" :disabled="!eventFilter">
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
        <el-button type="primary" @click="handleSearch" :loading="loading" :disabled="!eventFilter">
          搜索
        </el-button>
        <el-select
          v-model="eventFilter"
          placeholder="请选择赛事"
          style="width: 200px; margin-left: 10px;"
          @change="handleSearch"
        >
          <el-option
            v-for="event in eventList"
            :key="event.id"
            :label="event.name"
            :value="event.id"
          />
        </el-select>
        <span v-if="!eventFilter" class="event-hint">
          <el-icon><Warning /></el-icon>
          请选择具体赛事后再进行查询、录入或导出
        </span>
      </div>

      <!-- 成绩列表表格 -->
      <el-table
        ref="resultsTable"
        :data="results"
        v-loading="loading"
        stripe
        border
        style="width: 100%; margin-top: 20px;"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" align="center" />
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column label="赛事" min-width="180" show-overflow-tooltip>
          <template #default="{ row }">
            {{ row.event_title || '-' }}
          </template>
        </el-table-column>
        <el-table-column label="参赛者" width="120">
          <template #default="{ row }">
            {{ row.user_name || '-' }}
          </template>
        </el-table-column>
        <el-table-column label="轮次" width="100">
          <template #default="{ row }">
            <el-tag v-if="row.round_type === 'final'" type="danger">决赛</el-tag>
            <el-tag v-else-if="row.round_type === 'semifinal'" type="warning">半决赛</el-tag>
            <el-tag v-else type="info">初赛</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="score" label="成绩" width="120" />
        <el-table-column prop="rank" label="排名" width="100">
          <template #default="{ row }">
            <el-tag v-if="row.rank === 1" type="danger">第{{ row.rank }}名</el-tag>
            <el-tag v-else-if="row.rank === 2" type="warning">第{{ row.rank }}名</el-tag>
            <el-tag v-else-if="row.rank === 3" type="success">第{{ row.rank }}名</el-tag>
            <el-tag v-else type="info">第{{ row.rank }}名</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="是否公开" width="100">
          <template #default="{ row }">
            <el-switch
              v-model="row.is_published"
              @change="handlePublicChange(row)"
              :disabled="switchLoading[row.id]"
            />
          </template>
        </el-table-column>
        <el-table-column label="录入时间" width="180">
          <template #default="{ row }">
            {{ formatDateTime(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button
              type="primary"
              size="small"
              @click="handleEdit(row)"
            >
              编辑
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

    <!-- 录入/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="600px"
      @close="resetForm"
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="formRules"
        label-width="100px"
      >
        <el-form-item label="选择赛事" prop="event">
          <el-select
            v-model="form.event"
            placeholder="请选择赛事"
            style="width: 100%;"
            filterable
            @change="handleEventChange"
          >
            <el-option
              v-for="event in eventList"
              :key="event.id"
              :label="event.name"
              :value="event.id"
            />
          </el-select>
          <div style="color: #E6A23C; font-size: 12px; margin-top: 5px;">
            <el-icon style="vertical-align: middle;"><Warning /></el-icon>
            只能为进行中或已结束的赛事录入成绩
          </div>
        </el-form-item>

        <el-form-item label="选择参赛者" prop="registration">
          <el-select
            v-model="form.registration"
            placeholder="请先选择赛事"
            style="width: 100%;"
            filterable
            :disabled="!form.event"
            :loading="registrationLoading"
          >
            <el-option
              v-for="reg in registrationList"
              :key="reg.id"
              :label="`${reg.participant_name} (${reg.participant_phone})`"
              :value="reg.id"
            />
          </el-select>
          <div style="color: #909399; font-size: 12px; margin-top: 5px;">
            只显示已通过审核的报名记录
          </div>
        </el-form-item>

        <el-form-item label="轮次" prop="round_type">
          <el-select v-model="form.round_type" placeholder="请选择轮次" style="width: 100%;">
            <el-option label="决赛" value="final" />
            <el-option label="半决赛" value="semifinal" />
            <el-option label="初赛" value="preliminary" />
          </el-select>
        </el-form-item>

        <el-form-item label="成绩" prop="score">
          <el-input v-model="form.score" placeholder="请输入成绩" />
        </el-form-item>

        <el-form-item label="排名" prop="rank">
          <el-input-number
            v-model="form.rank"
            :min="1"
            placeholder="请输入排名"
            style="width: 100%;"
          />
        </el-form-item>

        <el-form-item label="奖项" prop="award">
          <el-input v-model="form.award" placeholder="如：金牌、一等奖等（可选）" />
        </el-form-item>

        <el-form-item label="是否公开" prop="is_published">
          <el-switch v-model="form.is_published" />
          <span style="margin-left: 10px; color: #909399; font-size: 12px;">
            公开后用户可在个人中心查看成绩
          </span>
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">
          确定
        </el-button>
      </template>
    </el-dialog>

    <!-- 批量导入对话框 -->
    <el-dialog
      v-model="importDialogVisible"
      title="批量导入成绩"
      width="520px"
      @close="resetImportDialog"
    >
      <div class="import-dialog">
        <el-upload
          :auto-upload="false"
          :file-list="importFileList"
          :before-upload="handleImportBeforeUpload"
          :on-change="handleImportChange"
          :on-remove="handleImportRemove"
          accept=".xlsx"
        >
          <el-button type="primary">选择文件</el-button>
          <div class="el-upload__tip">仅支持 .xlsx 文件，每次上传一个</div>
        </el-upload>
        <el-alert
          v-if="importSuccessCount"
          type="info"
          title="导入完成"
          :description="`已成功导入 ${importSuccessCount} 条成绩`"
          show-icon
        />
        <el-alert v-if="importResultErrors.length" title="部分行未导入" type="warning" show-icon>
          <div v-for="error in importResultErrors" :key="`import-error-${error.row}-${error.detail}`" class="import-error-item">
            第{{ error.row }}行：{{ error.detail }}
          </div>
        </el-alert>
      </div>
      <template #footer>
        <el-button @click="importDialogVisible = false">取消</el-button>
        <el-button
          type="primary"
          @click="handleImportSubmit"
          :loading="importLoading"
          :disabled="importLoading || !hasImportFiles"
        >
          确定
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search, Warning, Upload } from '@element-plus/icons-vue'
import {
  getResultList,
  createResult,
  updateResult,
  patchResult,
  deleteResult,
  publishResult,
  exportResults,
  importResults,
  bulkPublishResults,
  bulkDeleteResults
} from '@/api/result'
import { getEventList, getEventRegistrations } from '@/api/event'
import { getMyRefereeEvents } from '@/api/referee'

// 搜索和筛选
const searchQuery = ref('')
const eventFilter = ref('')

const store = useStore()
const isReferee = computed(() => store.state.user.userInfo?.user_type === 'referee')

// 成绩列表
const results = ref([])
const loading = ref(false)
const switchLoading = ref({})

// 赛事列表和报名列表
const eventList = ref([])
const registrationList = ref([])
const registrationLoading = ref(false)

// 分页
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const resultsTable = ref(null)
const selectedResults = ref([])
const hasSelection = computed(() => selectedResults.value.length > 0)

// 对话框
const dialogVisible = ref(false)
const dialogTitle = computed(() => form.id ? '编辑成绩' : '录入成绩')
const submitting = ref(false)
const formRef = ref(null)

// 表单数据
const form = reactive({
  id: null,
  event: '',
  registration: '',
  round_type: 'final',
  score: '',
  rank: 1,
  award: '',
  is_published: true
})

// 表单验证规则
const formRules = {
  event: [
    { required: true, message: '请选择赛事', trigger: 'change' }
  ],
  registration: [
    { required: true, message: '请选择参赛者', trigger: 'change' }
  ],
  round_type: [
    { required: true, message: '请选择轮次', trigger: 'change' }
  ],
  score: [
    { required: true, message: '请输入成绩', trigger: 'blur' }
  ],
  rank: [
    { required: true, message: '请输入排名', trigger: 'blur' }
  ]
}

// 批量导入相关
const importDialogVisible = ref(false)
const importLoading = ref(false)
const importFileList = ref([])
const importResultErrors = ref([])
const importSuccessCount = ref(0)
const hasImportFiles = computed(() => importFileList.value.length > 0)

const handleImportOpen = () => {
  if (!eventFilter.value) {
    ElMessage.warning('请先选择一个赛事，再导入成绩')
    return
  }
  resetImportDialog()
  importDialogVisible.value = true
}

const handleImportBeforeUpload = (file) => {
  importFileList.value = [file]
  return false
}

const handleImportChange = (file) => {
  importFileList.value = [file]
}

const handleImportRemove = () => {
  importFileList.value = []
}

const resetImportDialog = () => {
  importFileList.value = []
  importResultErrors.value = []
  importSuccessCount.value = 0
  importLoading.value = false
}

const handleSelectionChange = (selection) => {
  selectedResults.value = selection
}

const resetSelection = () => {
  selectedResults.value = []
  resultsTable.value?.clearSelection()
}

const handleImportSubmit = async () => {
  if (!importFileList.value.length) {
    ElMessage.warning('请先选择要导入的文件')
    return
  }
  importLoading.value = true
  try {
    const formData = new FormData()
    formData.append('file', importFileList.value[0].raw)
    if (eventFilter.value) {
      formData.append('context_event', eventFilter.value)
    }
    const response = await importResults(formData)
    importSuccessCount.value = response.imported || 0
    importResultErrors.value = response.errors || []
    if (importResultErrors.value.length) {
      ElMessage.warning('部分行导入失败，请查看详情')
    } else {
      ElMessage.success('批量导入完成')
      importDialogVisible.value = false
    }
    await fetchResults()
  } catch (error) {
    console.error('批量导入失败:', error)
    ElMessage.error(error.response?.data?.detail || error.response?.data?.error || '批量导入失败')
  } finally {
    importLoading.value = false
  }
}

// 获取成绩列表
const fetchResults = async () => {
  if (!eventFilter.value) {
    results.value = []
    total.value = 0
    ElMessage.warning('请先选择一个赛事，再查看该赛事的成绩')
    return
  }
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize.value
    }

    if (searchQuery.value) {
      params.search = searchQuery.value
    }

    if (eventFilter.value) {
      params.event = eventFilter.value
    }

    const response = await getResultList(params)
    results.value = response.results || []
    total.value = response.count || 0
  } catch (error) {
    console.error('获取成绩列表失败:', error)
    ElMessage.error('获取成绩列表失败')
  } finally {
    loading.value = false
  }
}

// 获取赛事列表
const fetchEvents = async () => {
  try {
    const allEvents = isReferee.value
      ? await getMyRefereeEvents()
      : (await getEventList({ page_size: 1000 })).results || []
    const now = new Date()
    eventList.value = (allEvents || []).filter(event => {
      const startTime = new Date(event.start_time)
      return now >= startTime
    })

    if (eventList.value.length === 0) {
      ElMessage.warning('暂无可录入成绩的赛事，只能为进行中或已结束的赛事录入成绩')
    }
  } catch (error) {
    console.error('获取赛事列表失败:', error)
  }
}

// 获取赛事的已通过报名列表
const fetchRegistrations = async (eventId) => {
  if (!eventId) {
    registrationList.value = []
    return
  }

  registrationLoading.value = true
  try {
    const response = await getEventRegistrations(eventId)
    registrationList.value = (response || []).filter(reg => reg.status === 'approved')
  } catch (error) {
    console.error('获取报名列表失败:', error)
    ElMessage.error('获取报名列表失败')
  } finally {
    registrationLoading.value = false
  }
}

// 赛事变化处理
const handleEventChange = (eventId) => {
  form.registration = ''
  registrationList.value = []
  if (eventId) {
    fetchRegistrations(eventId)
  }
}

// 搜索处理
const handleSearch = () => {
  currentPage.value = 1
  fetchResults()
}

// 分页大小变化
const handleSizeChange = (newSize) => {
  pageSize.value = newSize
  currentPage.value = 1
  fetchResults()
}

// 页码变化
const handlePageChange = (newPage) => {
  currentPage.value = newPage
  fetchResults()
}

// 录入成绩
const handleAdd = () => {
  if (!eventFilter.value) {
    ElMessage.warning('请先选择一个赛事，再录入成绩')
    return
  }
  resetForm()
  form.event = eventFilter.value
  handleEventChange(eventFilter.value)
  dialogVisible.value = true
}

// 编辑成绩
const handleEdit = async (result) => {
  form.id = result.id
  form.event = result.event
  form.registration = result.registration
  form.round_type = result.round_type || 'final'
  form.score = result.score
  form.rank = result.rank
  form.award = result.award || ''
  form.is_published = result.is_published

  // 加载该赛事的报名列表
  await fetchRegistrations(result.event)

  dialogVisible.value = true
}

// 提交表单
const handleSubmit = async () => {
  try {
    await formRef.value.validate()

    submitting.value = true

    const data = {
      event: form.event,
      registration: form.registration,
      round_type: form.round_type,
      score: form.score,
      rank: form.rank,
      award: form.award,
      is_published: form.is_published
    }

    if (form.id) {
      // 编辑
      await updateResult(form.id, data)
      ElMessage.success('成绩更新成功')
    } else {
      // 新增
      await createResult(data)
      ElMessage.success('成绩录入成功')
    }

    dialogVisible.value = false
    await fetchResults()
  } catch (error) {
    if (error.message) {
      console.error('提交失败:', error)
      ElMessage.error(error.response?.data?.detail || error.response?.data?.error || '提交失败')
    }
  } finally {
    submitting.value = false
  }
}

// 公开状态切换
const handlePublicChange = async (result) => {
  switchLoading.value[result.id] = true
  try {
    await patchResult(result.id, { is_published: result.is_published })
    ElMessage.success(result.is_published ? '已公开成绩' : '已取消公开')
  } catch (error) {
    // 恢复原状态
    result.is_published = !result.is_published
    console.error('更新失败:', error)
    ElMessage.error('更新失败')
  } finally {
    switchLoading.value[result.id] = false
  }
}

// 删除成绩
const handleDelete = async (result) => {
  try {
    await ElMessageBox.confirm(
      `确认删除该成绩记录吗？此操作不可恢复！`,
      '删除确认',
      {
        confirmButtonText: '确认删除',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'el-button--danger'
      }
    )

    await deleteResult(result.id)
    ElMessage.success('成绩删除成功')
    await fetchResults()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除成绩失败:', error)
      ElMessage.error(error.response?.data?.detail || error.response?.data?.error || '删除成绩失败')
    }
  }
}

// 批量公开成绩
const handleBulkPublish = async () => {
  const ids = selectedResults.value.map(result => result.id)
  if (!ids.length) {
    ElMessage.info('请先勾选需要公开的成绩')
    return
  }

  try {
    await ElMessageBox.confirm(
      `确认公开选中的 ${ids.length} 条成绩记录吗？此操作不可恢复！`,
      '批量公开确认',
      {
        confirmButtonText: '确认公开',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'el-button--success'
      }
    )

    await bulkPublishResults(ids)
    ElMessage.success('批量公开成功')
    resetSelection()
    await fetchResults()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('批量公开失败:', error)
      ElMessage.error('批量公开失败')
    }
  }
}

// 批量删除成绩
const handleBulkDelete = async () => {
  const ids = selectedResults.value.map(result => result.id)
  if (!ids.length) {
    ElMessage.info('请先勾选需要删除的成绩')
    return
  }

  try {
    await ElMessageBox.confirm(
      `确认删除选中的 ${ids.length} 条成绩记录吗？此操作不可恢复！`,
      '批量删除确认',
      {
        confirmButtonText: '确认删除',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'el-button--danger'
      }
    )

    await bulkDeleteResults(ids)
    ElMessage.success('批量删除成功')
    resetSelection()
    await fetchResults()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('批量删除失败:', error)
      ElMessage.error('批量删除失败')
    }
  }
}

// 重置表单
const resetForm = () => {
  form.id = null
  form.event = ''
  form.registration = ''
  form.round_type = 'final'
  form.score = ''
  form.rank = 1
  form.award = ''
  form.is_published = true
  registrationList.value = []
  formRef.value?.clearValidate()
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
  fetchEvents()
})
</script>

<style scoped>
.results-page {
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

.event-hint {
  color: #e6a23c;
  font-size: 12px;
  margin-left: 10px;
  display: flex;
  align-items: center;
}

.import-dialog {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.import-error-item {
  font-size: 12px;
  color: #f56c6c;
}

@media (max-width: 768px) {
  .results-page {
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

  .card-header > div {
    width: 100%;
    display: flex;
    justify-content: space-between;
  }
}
</style>
