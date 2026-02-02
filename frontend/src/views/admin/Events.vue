<template>
  <div class="events-page">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>赛事管理</span>
          <div>
            <el-button type="primary" icon="Refresh" @click="fetchEvents" :loading="loading">
              刷新
            </el-button>
            <el-button type="success" icon="Plus" @click="handleAdd">
              新增赛事
            </el-button>
          </div>
        </div>
      </template>

      <!-- 搜索和筛选区域 -->
      <div class="search-bar">
        <el-input
          v-model="searchQuery"
          placeholder="搜索赛事名称、地点"
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
          placeholder="赛事状态"
          clearable
          style="width: 150px; margin-left: 10px;"
          @change="handleSearch"
        >
          <el-option label="全部" value="" />
          <el-option label="草稿" value="draft" />
          <el-option label="已发布" value="published" />
          <el-option label="进行中" value="ongoing" />
          <el-option label="已结束" value="finished" />
          <el-option label="已取消" value="cancelled" />
        </el-select>
      </div>

      <!-- 赛事列表表格 -->
      <el-table
        :data="events"
        v-loading="loading"
        stripe
        style="width: 100%; margin-top: 20px;"
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column label="图片" width="100">
          <template #default="{ row }">
            <el-image
              v-if="row.image"
              :src="row.image"
              :preview-src-list="[row.image]"
              :preview-teleported="true"
              fit="cover"
              style="width: 60px; height: 60px; border-radius: 4px;"
            />
            <span v-else style="color: #999;">无图片</span>
          </template>
        </el-table-column>
        <el-table-column prop="title" label="赛事名称" min-width="180" show-overflow-tooltip />
        <el-table-column label="比赛时间" width="320">
          <template #default="{ row }">
            {{ formatDateTime(row.start_time) }} 至 {{ formatDateTime(row.end_time) }}
          </template>
        </el-table-column>
        <el-table-column prop="location" label="参赛地点" min-width="150" show-overflow-tooltip />
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusMeta(row).type">
              {{ getStatusMeta(row).label }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="{ row }">
            {{ formatDateTime(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="300" fixed="right">
          <template #default="{ row }">
            <el-button
              type="primary"
              size="small"
              @click="handleEdit(row)"
            >
              编辑
            </el-button>
            <el-button
              v-if="row.status === 'draft'"
              type="success"
              size="small"
              @click="handlePublish(row)"
            >
              发布
            </el-button>
            <el-button
              v-if="row.status === 'published'"
              type="warning"
              size="small"
              @click="handleUnpublish(row)"
            >
              取消发布
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

    <!-- 新增/编辑对话框 -->
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
        <el-form-item label="赛事名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入赛事名称" />
        </el-form-item>

        <el-form-item label="赛事图片" prop="image">
          <el-upload
            class="event-uploader"
            :action="uploadUrl"
            :headers="uploadHeaders"
            :show-file-list="false"
            :on-success="handleUploadSuccess"
            :before-upload="beforeUpload"
            accept="image/*"
          >
            <img v-if="form.image" :src="form.image" class="event-image" />
            <el-icon v-else class="event-uploader-icon"><Plus /></el-icon>
          </el-upload>
          <div class="upload-tip">点击上传图片，支持jpg/png格式，大小不超过2MB</div>
        </el-form-item>

        <el-form-item label="比赛时间">
          <el-col :span="11">
            <el-form-item prop="start_time">
              <el-date-picker
                v-model="form.start_time"
                type="datetime"
                placeholder="开始时间"
                format="YYYY-MM-DD HH:mm"
                value-format="YYYY-MM-DD HH:mm:ss"
                style="width: 100%;"
              />
            </el-form-item>
          </el-col>
          <el-col :span="2" style="text-align: center;">至</el-col>
          <el-col :span="11">
            <el-form-item prop="end_time">
              <el-date-picker
                v-model="form.end_time"
                type="datetime"
                placeholder="结束时间"
                format="YYYY-MM-DD HH:mm"
                value-format="YYYY-MM-DD HH:mm:ss"
                style="width: 100%;"
              />
            </el-form-item>
          </el-col>
        </el-form-item>

        <el-form-item label="报名时间">
          <el-col :span="11">
            <el-date-picker
              v-model="form.registration_start"
              type="datetime"
              placeholder="报名开始时间"
              format="YYYY-MM-DD HH:mm"
              value-format="YYYY-MM-DD HH:mm:ss"
              style="width: 100%;"
            />
          </el-col>
          <el-col :span="2" style="text-align: center;">至</el-col>
          <el-col :span="11">
            <el-date-picker
              v-model="form.registration_end"
              type="datetime"
              placeholder="报名结束时间"
              format="YYYY-MM-DD HH:mm"
              value-format="YYYY-MM-DD HH:mm:ss"
              style="width: 100%;"
            />
          </el-col>
        </el-form-item>

        <el-form-item label="联系人">
          <el-input v-model="form.contact_person" placeholder="请输入联系人" />
        </el-form-item>

        <el-form-item label="联系电话">
          <el-input v-model="form.contact_phone" placeholder="请输入联系电话" />
        </el-form-item>

        <el-form-item label="参赛地点" prop="location">
          <el-input v-model="form.location" placeholder="请输入参赛地点" />
        </el-form-item>

        <el-form-item label="详情介绍" prop="description">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="4"
            placeholder="请输入详情介绍"
          />
        </el-form-item>

        <el-form-item label="状态" prop="status">
          <el-select v-model="form.status" placeholder="请选择状态" style="width: 100%;">
            <el-option label="草稿" value="draft" />
            <el-option label="已发布" value="published" />
            <el-option label="进行中" value="ongoing" />
            <el-option label="已结束" value="finished" />
            <el-option label="已取消" value="cancelled" />
          </el-select>
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">
          确定
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search, Plus } from '@element-plus/icons-vue'
import { useStore } from 'vuex'
import { getEventList, createEvent, updateEvent, deleteEvent, publishEvent, unpublishEvent } from '@/api/event'

const store = useStore()
const token = computed(() => store.state.user.token)


// 搜索和筛选
const searchQuery = ref('')
const statusFilter = ref('')

// 赛事列表
const events = ref([])
const loading = ref(false)

// 分页
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

// 对话框
const dialogVisible = ref(false)
const dialogTitle = computed(() => form.id ? '编辑赛事' : '新增赛事')
const submitting = ref(false)
const formRef = ref(null)

// 表单数据
const form = reactive({
  id: null,
  name: '',
  image: '',
  start_time: '',
  end_time: '',
  location: '',
  description: '',
  status: 'draft',
  event_type: 'athletics',  // 默认田径
  registration_start: '',
  registration_end: '',
  contact_person: '',
  contact_phone: ''
})

// 状态标签映射
const STATUS_TAGS = {
  draft: { label: '草稿', type: 'info' },
  published: { label: '已发布', type: 'success' },
  ongoing: { label: '进行中', type: 'success' },
  finished: { label: '已结束', type: 'warning' },
  cancelled: { label: '已取消', type: 'danger' },
  default: { label: '未知状态', type: 'info' }
}

// 获取状态标签
const getStatusMeta = (row) => {
  const key = row.display_status || row.status
  return STATUS_TAGS[key] || STATUS_TAGS.default
}

// 表单验证规则
const formRules = {
  name: [
    { required: true, message: '请输入赛事名称', trigger: 'blur' }
  ],
  start_time: [
    { required: true, message: '请选择比赛开始时间', trigger: 'change' }
  ],
  end_time: [
    { required: true, message: '请选择比赛结束时间', trigger: 'change' },
    {
      validator: (rule, value, callback) => {
        if (form.start_time && value) {
          if (new Date(value) <= new Date(form.start_time)) {
            callback(new Error('结束时间必须晚于开始时间'))
          } else {
            callback()
          }
        } else {
          callback()
        }
      },
      trigger: 'change'
    }
  ],
  location: [
    { required: true, message: '请输入参赛地点', trigger: 'blur' }
  ],
  contact_person: [
    { required: true, message: '请输入联系人', trigger: 'blur' }
  ],
  contact_phone: [
    { required: true, message: '请输入联系电话', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
  ],
  status: [
    { required: true, message: '请选择状态', trigger: 'change' }
  ]
}

// 上传配置
const uploadUrl = computed(() => {
  return import.meta.env.VITE_API_BASE_URL + '/events/upload_image/'
})

const uploadHeaders = computed(() => {
  return {
    'Authorization': `Bearer ${token.value}`
  }
})

// 上传成功回调
const handleUploadSuccess = (response) => {
  if (response.image) {
    form.image = response.image
    ElMessage.success('图片上传成功')
  }
}

// 上传前验证
const beforeUpload = (file) => {
  const isImage = file.type.startsWith('image/')
  const isLt2M = file.size / 1024 / 1024 < 2

  if (!isImage) {
    ElMessage.error('只能上传图片文件!')
    return false
  }
  if (!isLt2M) {
    ElMessage.error('图片大小不能超过 2MB!')
    return false
  }
  return true
}

// 获取赛事列表
const fetchEvents = async () => {
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

    const response = await getEventList(params)
    events.value = response.results || []
    total.value = response.count || 0
  } catch (error) {
    console.error('获取赛事列表失败:', error)
    ElMessage.error('获取赛事列表失败')
  } finally {
    loading.value = false
  }
}

// 搜索处理
const handleSearch = () => {
  currentPage.value = 1
  fetchEvents()
}

// 分页大小变化
const handleSizeChange = (newSize) => {
  pageSize.value = newSize
  currentPage.value = 1
  fetchEvents()
}

// 页码变化
const handlePageChange = (newPage) => {
  currentPage.value = newPage
  fetchEvents()
}

// 新增赛事
const handleAdd = () => {
  resetForm()
  dialogVisible.value = true
}

// 编辑赛事
const handleEdit = (event) => {
  form.id = event.id
  form.name = event.title  // title → name（前端字段）
  form.image = event.cover_image  // cover_image → image
  form.start_time = event.start_time
  form.end_time = event.end_time
  form.location = event.location
  form.description = event.description || ''
  form.status = event.status
  form.event_type = event.event_type || 'athletics'
  form.registration_start = event.registration_start
  form.registration_end = event.registration_end
  form.contact_person = event.contact_person || ''
  form.contact_phone = event.contact_phone || ''
  dialogVisible.value = true
}

// 提交表单
const handleSubmit = async () => {
  try {
    await formRef.value.validate()

    submitting.value = true

    const formData = new FormData()
    formData.append('title', form.name)  // name → title

    // 格式化日期时间为ISO格式
    const formatDateTime = (dateTime) => {
      if (!dateTime) return ''
      if (typeof dateTime === 'string') return dateTime
      // Date对象转ISO字符串
      return new Date(dateTime).toISOString()
    }

    formData.append('start_time', formatDateTime(form.start_time))
    formData.append('end_time', formatDateTime(form.end_time))
    formData.append('location', form.location)
    formData.append('description', form.description || '')
    formData.append('status', form.status)

    // 添加必填字段
    formData.append('event_type', form.event_type || 'athletics')
    formData.append('registration_start', formatDateTime(form.registration_start || form.start_time))
    formData.append('registration_end', formatDateTime(form.registration_end || form.end_time))
    formData.append('contact_person', form.contact_person)
    formData.append('contact_phone', form.contact_phone)

    if (form.image) {
      formData.append('cover_image', form.image)  // image → cover_image
    }

    if (form.id) {
      // 编辑
      await updateEvent(form.id, formData)
      ElMessage.success('赛事更新成功')
    } else {
      // 新增
      await createEvent(formData)
      ElMessage.success('赛事创建成功')
    }

    dialogVisible.value = false
    await fetchEvents()
  } catch (error) {
    if (error.message) {
      console.error('提交失败:', error)
      ElMessage.error(error.response?.data?.error || '提交失败')
    }
  } finally {
    submitting.value = false
  }
}

// 发布赛事
const handlePublish = async (event) => {
  try {
    await ElMessageBox.confirm('确认发布该赛事？', '提示', {
      confirmButtonText: '确认',
      cancelButtonText: '取消',
      type: 'success'
    })

    await publishEvent(event.id)
    ElMessage.success('赛事发布成功')
    await fetchEvents()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('发布失败:', error)
      ElMessage.error(error.response?.data?.error || '发布失败')
    }
  }
}

// 取消发布
const handleUnpublish = async (event) => {
  try {
    await ElMessageBox.confirm('确认取消发布该赛事？', '提示', {
      confirmButtonText: '确认',
      cancelButtonText: '取消',
      type: 'warning'
    })

    await unpublishEvent(event.id)
    ElMessage.success('已取消发布')
    await fetchEvents()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('取消发布失败:', error)
      ElMessage.error(error.response?.data?.error || '取消发布失败')
    }
  }
}

// 删除赛事
const handleDelete = async (event) => {
  try {
    await ElMessageBox.confirm(
      `确认删除赛事 "${event.title}" 吗？此操作不可恢复！`,
      '删除确认',
      {
        confirmButtonText: '确认删除',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'el-button--danger'
      }
    )

    await deleteEvent(event.id)
    ElMessage.success('赛事删除成功')
    await fetchEvents()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除赛事失败:', error)
      ElMessage.error(error.response?.data?.error || '删除赛事失败')
    }
  }
}

// 重置表单
const resetForm = () => {
  form.id = null
  form.name = ''
  form.image = ''
  form.start_time = ''
  form.end_time = ''
  form.location = ''
  form.description = ''
  form.status = 'draft'
  form.contact_person = ''
  form.contact_phone = ''
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
.events-page {
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

.event-uploader {
  width: 100%;
}

.event-uploader :deep(.el-upload) {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: all 0.3s;
  width: 178px;
  height: 178px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.event-uploader :deep(.el-upload:hover) {
  border-color: #409EFF;
}

.event-uploader-icon {
  font-size: 28px;
  color: #8c939d;
}

.event-image {
  width: 178px;
  height: 178px;
  display: block;
  object-fit: cover;
}

.upload-tip {
  font-size: 12px;
  color: #999;
  margin-top: 5px;
}

@media (max-width: 768px) {
  .events-page {
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
