<template>
  <div class="announcements-page">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>公告管理</span>
          <div>
            <el-button type="primary" icon="Refresh" @click="fetchAnnouncements" :loading="loading">
              刷新
            </el-button>
            <el-button type="success" icon="Plus" @click="handleAdd">
              新增公告
            </el-button>
          </div>
        </div>
      </template>

      <!-- 搜索区域 -->
      <div class="search-bar">
        <el-input
          v-model="searchQuery"
          placeholder="搜索公告标题"
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
      </div>

      <!-- 公告列表表格 -->
      <el-table
        :data="announcements"
        v-loading="loading"
        stripe
        border
        style="width: 100%; margin-top: 20px;"
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column label="封面" width="100">
          <template #default="{ row }">
            <el-image
              v-if="row.image"
              :src="row.image"
              :preview-src-list="[row.image]"
              fit="cover"
              style="width: 60px; height: 60px; border-radius: 4px;"
            />
            <span v-else style="color: #999;">无图片</span>
          </template>
        </el-table-column>
        <el-table-column prop="title" label="标题" min-width="200" show-overflow-tooltip />
        <el-table-column label="摘要" min-width="250" show-overflow-tooltip>
          <template #default="{ row }">
            {{ row.summary || '-' }}
          </template>
        </el-table-column>
        <el-table-column prop="views" label="浏览量" width="100" align="center" />
        <el-table-column label="置顶" width="80" align="center">
          <template #default="{ row }">
            <el-tag v-if="row.is_pinned" type="danger" size="small">置顶</el-tag>
            <el-tag v-else type="info" size="small">否</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag v-if="row.status === 'draft'" type="info">草稿</el-tag>
            <el-tag v-else-if="row.status === 'published'" type="success">已发布</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="发布时间" width="180">
          <template #default="{ row }">
            {{ formatDateTime(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="250" fixed="right">
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
              v-else
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
      width="800px"
      @close="resetForm"
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="formRules"
        label-width="100px"
      >
        <el-form-item label="标题" prop="title">
          <el-input v-model="form.title" placeholder="请输入公告标题" maxlength="100" show-word-limit />
        </el-form-item>

        <el-form-item label="摘要" prop="summary">
          <el-input
            v-model="form.summary"
            type="textarea"
            :rows="2"
            placeholder="请输入公告摘要"
            maxlength="200"
            show-word-limit
          />
        </el-form-item>

        <el-form-item label="封面图片" prop="image">
          <el-upload
            class="announcement-uploader"
            :action="uploadUrl"
            :headers="uploadHeaders"
            :show-file-list="false"
            :on-success="handleUploadSuccess"
            :before-upload="beforeUpload"
            accept="image/*"
          >
            <img v-if="form.image" :src="form.image" class="announcement-image" />
            <el-icon v-else class="announcement-uploader-icon"><Plus /></el-icon>
          </el-upload>
          <div class="upload-tip">点击上传封面图片，支持jpg/png格式，大小不超过2MB</div>
        </el-form-item>

        <el-form-item label="内容" prop="content">
          <el-input
            v-model="form.content"
            type="textarea"
            :rows="8"
            placeholder="请输入公告内容"
          />
        </el-form-item>

        <el-form-item label="是否置顶" prop="is_pinned">
          <el-switch v-model="form.is_pinned" />
        </el-form-item>

        <el-form-item label="状态" prop="status">
          <el-select v-model="form.status" placeholder="请选择状态" style="width: 100%;">
            <el-option label="草稿" value="draft" />
            <el-option label="已发布" value="published" />
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
import { getAnnouncementList, createAnnouncement, updateAnnouncement, deleteAnnouncement, publishAnnouncement, getAnnouncementDetail } from '@/api/announcement'
import { getToken } from '@/utils/auth'

// 搜索
const searchQuery = ref('')

// 公告列表
const announcements = ref([])
const loading = ref(false)

// 分页
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

// 对话框
const dialogVisible = ref(false)
const dialogTitle = computed(() => form.id ? '编辑公告' : '新增公告')
const submitting = ref(false)
const formRef = ref(null)

// 表单数据
const form = reactive({
  id: null,
  title: '',
  summary: '',
  image: '',
  content: '',
  is_pinned: false,
  status: 'draft'
})

// 表单验证规则
const formRules = {
  title: [
    { required: true, message: '请输入公告标题', trigger: 'blur' }
  ],
  summary: [
    { required: true, message: '请输入公告摘要', trigger: 'blur' }
  ],
  content: [
    { required: true, message: '请输入公告内容', trigger: 'blur' }
  ],
  status: [
    { required: true, message: '请选择状态', trigger: 'change' }
  ]
}

// 上传配置
const uploadUrl = computed(() => {
  return import.meta.env.VITE_API_BASE_URL + '/announcements/upload_image/'
})

const uploadHeaders = computed(() => {
  return {
    'Authorization': `Bearer ${getToken()}`
  }
})

// 获取公告列表
const fetchAnnouncements = async () => {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize.value
    }

    if (searchQuery.value) {
      params.search = searchQuery.value
    }

    const response = await getAnnouncementList(params)
    announcements.value = response.results || []
    total.value = response.count || 0
  } catch (error) {
    console.error('获取公告列表失败:', error)
    ElMessage.error('获取公告列表失败')
  } finally {
    loading.value = false
  }
}

// 搜索处理
const handleSearch = () => {
  currentPage.value = 1
  fetchAnnouncements()
}

// 分页大小变化
const handleSizeChange = (newSize) => {
  pageSize.value = newSize
  currentPage.value = 1
  fetchAnnouncements()
}

// 页码变化
const handlePageChange = (newPage) => {
  currentPage.value = newPage
  fetchAnnouncements()
}

// 新增公告
const handleAdd = () => {
  resetForm()
  dialogVisible.value = true
}

// 编辑公告
const handleEdit = async (announcement) => {
  resetForm()
  try {
    const detail = await getAnnouncementDetail(announcement.id)
    form.id = detail.id
    form.title = detail.title
    form.summary = detail.summary || ''
    form.image = detail.image || detail.cover_image || ''
    form.content = detail.content || ''
    form.is_pinned = detail.is_pinned
    form.status = detail.status || 'draft'
    dialogVisible.value = true
  } catch (error) {
    console.error('获取公告详情失败:', error)
    ElMessage.error('获取公告详情失败')
  }
}

// 提交表单
const handleSubmit = async () => {
  try {
    await formRef.value.validate()

    submitting.value = true

    const data = {
      title: form.title,
      summary: form.summary,
      content: form.content,
      is_pinned: form.is_pinned,
      status: form.status
    }

    if (form.image) {
      data.image = form.image
    }

    if (form.id) {
      // 编辑
      await updateAnnouncement(form.id, data)
      ElMessage.success('公告更新成功')
    } else {
      // 新增
      await createAnnouncement(data)
      ElMessage.success('公告创建成功')
    }

    dialogVisible.value = false
    await fetchAnnouncements()
  } catch (error) {
    if (error.message) {
      console.error('提交失败:', error)
      ElMessage.error(error.response?.data?.detail || error.response?.data?.error || '提交失败')
    }
  } finally {
    submitting.value = false
  }
}

// 上传成功
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

// 发布公告
const handlePublish = async (announcement) => {
  try {
    await ElMessageBox.confirm('确认发布该公告？', '提示', {
      confirmButtonText: '确认',
      cancelButtonText: '取消',
      type: 'success'
    })

    await publishAnnouncement(announcement.id)
    ElMessage.success('公告发布成功')
    await fetchAnnouncements()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('发布失败:', error)
      ElMessage.error(error.response?.data?.detail || error.response?.data?.error || '发布失败')
    }
  }
}

// 取消发布
const handleUnpublish = async (announcement) => {
  try {
    await ElMessageBox.confirm('确认取消发布该公告？', '提示', {
      confirmButtonText: '确认',
      cancelButtonText: '取消',
      type: 'warning'
    })

    await updateAnnouncement(announcement.id, { status: 'draft' })
    ElMessage.success('已取消发布')
    await fetchAnnouncements()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('取消发布失败:', error)
      ElMessage.error(error.response?.data?.detail || error.response?.data?.error || '取消发布失败')
    }
  }
}

// 删除公告
const handleDelete = async (announcement) => {
  try {
    await ElMessageBox.confirm(
      `确认删除公告 "${announcement.title}" 吗？此操作不可恢复！`,
      '删除确认',
      {
        confirmButtonText: '确认删除',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'el-button--danger'
      }
    )

    await deleteAnnouncement(announcement.id)
    ElMessage.success('公告删除成功')
    await fetchAnnouncements()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除公告失败:', error)
      ElMessage.error(error.response?.data?.detail || error.response?.data?.error || '删除公告失败')
    }
  }
}

// 重置表单
const resetForm = () => {
  form.id = null
  form.title = ''
  form.summary = ''
  form.image = ''
  form.content = ''
  form.is_pinned = false
  form.status = 'draft'
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
  fetchAnnouncements()
})
</script>

<style scoped>
.announcements-page {
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

.announcement-uploader {
  width: 100%;
}

.announcement-uploader :deep(.el-upload) {
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

.announcement-uploader :deep(.el-upload:hover) {
  border-color: #409EFF;
}

.announcement-uploader-icon {
  font-size: 28px;
  color: #8c939d;
}

.announcement-image {
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
  .announcements-page {
    padding: 10px;
  }

  .search-bar {
    flex-direction: column;
    align-items: stretch;
  }

  .search-bar .el-input {
    width: 100% !important;
    margin-right: 0 !important;
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
