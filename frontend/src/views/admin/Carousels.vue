<template>
  <div class="carousels-page">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>轮播图管理</span>
          <div>
            <el-button type="primary" icon="Refresh" @click="fetchCarousels" :loading="loading">
              刷新
            </el-button>
            <el-button type="success" icon="Plus" @click="handleAdd">
              新增轮播图
            </el-button>
          </div>
        </div>
      </template>

      <!-- 轮播图列表表格 -->
      <el-table
        :data="carousels"
        v-loading="loading"
        stripe
        border
        style="width: 100%; margin-top: 20px;"
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column label="预览图" width="200">
          <template #default="{ row }">
            <el-image
              v-if="row.image"
              :src="row.image"
              :preview-src-list="[row.image]"
              fit="cover"
              style="width: 160px; height: 60px; border-radius: 4px;"
            />
            <span v-else style="color: #999;">无图片</span>
          </template>
        </el-table-column>
        <el-table-column prop="title" label="标题" min-width="200" show-overflow-tooltip />
        <el-table-column label="链接" min-width="250" show-overflow-tooltip>
          <template #default="{ row }">
            <el-link v-if="row.link_url" :href="row.link_url" target="_blank" type="primary">
              {{ row.link_url }}
            </el-link>
            <span v-else style="color: #999;">-</span>
          </template>
        </el-table-column>
        <el-table-column prop="order" label="排序" width="100" align="center" sortable />
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-switch
              v-model="row.is_active"
              @change="handleStatusChange(row)"
              :disabled="switchLoading[row.id]"
            />
          </template>
        </el-table-column>
        <el-table-column label="创建时间" width="180">
          <template #default="{ row }">
            {{ formatDateTime(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="250" fixed="right">
          <template #default="{ row, $index }">
            <el-button
              type="primary"
              size="small"
              @click="handleEdit(row)"
            >
              编辑
            </el-button>
            <el-button
              type="info"
              size="small"
              @click="handleMoveUp(row, $index)"
              :disabled="$index === 0"
            >
              上移
            </el-button>
            <el-button
              type="info"
              size="small"
              @click="handleMoveDown(row, $index)"
              :disabled="$index === carousels.length - 1"
            >
              下移
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
        <el-form-item label="标题" prop="title">
          <el-input v-model="form.title" placeholder="请输入轮播图标题" maxlength="100" show-word-limit />
        </el-form-item>

        <el-form-item label="图片" prop="image">
          <el-upload
            class="carousel-uploader"
            :action="uploadUrl"
            :headers="uploadHeaders"
            :show-file-list="false"
            :on-success="handleUploadSuccess"
            :before-upload="beforeUpload"
            accept="image/*"
          >
            <img v-if="imagePreview" :src="imagePreview" class="carousel-image" />
            <el-icon v-else class="carousel-uploader-icon"><Plus /></el-icon>
          </el-upload>
          <div class="upload-tip">
            推荐尺寸：1920x600，点击上传图片，支持jpg/png/gif/webp格式，大小不超过5MB
          </div>
        </el-form-item>

        <el-form-item label="链接" prop="link">
          <el-input v-model="form.link" placeholder="可选，点击轮播图跳转的URL" />
        </el-form-item>

        <el-form-item label="排序序号" prop="order">
          <el-input-number
            v-model="form.order"
            :min="0"
            :max="999"
            placeholder="越小越靠前"
            style="width: 100%;"
          />
          <div class="form-tip">数字越小越靠前显示</div>
        </el-form-item>

        <el-form-item label="是否启用" prop="is_active">
          <el-switch v-model="form.is_active" />
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
import { Plus } from '@element-plus/icons-vue'
import { getCarouselList, createCarousel, updateCarousel, deleteCarousel, updateCarouselStatus } from '@/api/carousel'
import { getToken } from '@/utils/auth'

// 轮播图列表
const carousels = ref([])
const loading = ref(false)
const switchLoading = ref({})

// 对话框
const dialogVisible = ref(false)
const dialogTitle = computed(() => form.id ? '编辑轮播图' : '新增轮播图')
const submitting = ref(false)
const formRef = ref(null)

// 表单数据
const form = reactive({
  id: null,
  title: '',
  image: '',
  link: '',
  position: 'home',
  order: 0,
  is_active: true
})

// 图片预览和文件对象
const imagePreview = ref('')

// 表单验证规则
const formRules = {
  title: [
    { required: true, message: '请输入轮播图标题', trigger: 'blur' }
  ],
  image: [
    { required: true, message: '请上传轮播图图片', trigger: 'change' }
  ],
  order: [
    { required: true, message: '请输入排序序号', trigger: 'blur' }
  ]
}

// 上传配置
const uploadUrl = computed(() => {
  return import.meta.env.VITE_API_BASE_URL + '/carousels/upload_image/'
})

const uploadHeaders = computed(() => {
  return {
    'Authorization': `Bearer ${getToken()}`
  }
})

// 上传成功回调
const handleUploadSuccess = (response) => {
  if (response.image) {
    form.image = response.image
    imagePreview.value = response.image
    ElMessage.success('图片上传成功')
  }
}

// 上传前验证
const beforeUpload = (file) => {
  const isImage = file.type.startsWith('image/')
  const isLt5M = file.size / 1024 / 1024 < 5

  if (!isImage) {
    ElMessage.error('只能上传图片文件!')
    return false
  }
  if (!isLt5M) {
    ElMessage.error('图片大小不能超过 5MB!')
    return false
  }
  return true
}

// 获取轮播图列表
const fetchCarousels = async () => {
  loading.value = true
  try {
    const response = await getCarouselList({ page_size: 1000, ordering: 'order' })
    carousels.value = response.results || []
  } catch (error) {
    console.error('获取轮播图列表失败:', error)
    ElMessage.error('获取轮播图列表失败')
  } finally {
    loading.value = false
  }
}

// 新增轮播图
const handleAdd = () => {
  resetForm()
  dialogVisible.value = true
}

// 编辑轮播图
const handleEdit = (carousel) => {
  form.id = carousel.id
  form.title = carousel.title
  form.image = carousel.image
  form.link = carousel.link_url || ''
  form.position = carousel.position || 'home'
  form.order = carousel.order
  form.is_active = carousel.is_active
  imagePreview.value = carousel.image
  dialogVisible.value = true
}

// 提交表单
const handleSubmit = async () => {
  try {
    await formRef.value.validate()

    submitting.value = true

    const data = {
      title: form.title,
      image: form.image,
      link_url: form.link || '',
      position: form.position || 'home',
      order: form.order,
      is_active: form.is_active
    }

    if (form.id) {
      // 编辑
      await updateCarousel(form.id, data)
      ElMessage.success('轮播图更新成功')
    } else {
      // 新增
      await createCarousel(data)
      ElMessage.success('轮播图创建成功')
    }

    dialogVisible.value = false
    await fetchCarousels()
  } catch (error) {
    console.error('提交失败:', error)
    console.error('错误详情:', error.response?.data)

    // 显示详细错误信息
    let errorMsg = '提交失败'
    if (error.response?.data) {
      const errorData = error.response.data
      if (typeof errorData === 'object') {
        // 处理字段验证错误
        const errors = []
        for (const [field, messages] of Object.entries(errorData)) {
          if (Array.isArray(messages)) {
            errors.push(`${field}: ${messages.join(', ')}`)
          } else {
            errors.push(`${field}: ${messages}`)
          }
        }
        errorMsg = errors.join('\n') || errorMsg
      } else {
        errorMsg = errorData.detail || errorData.error || errorData
      }
    }
    ElMessage.error(errorMsg)
  } finally {
    submitting.value = false
  }
}

// 状态切换
const handleStatusChange = async (carousel) => {
  switchLoading.value[carousel.id] = true
  try {
    await updateCarouselStatus(carousel.id, carousel.is_active)
    ElMessage.success(carousel.is_active ? '已启用' : '已禁用')
  } catch (error) {
    // 恢复原状态
    carousel.is_active = !carousel.is_active
    console.error('更新失败:', error)
    ElMessage.error('更新失败')
  } finally {
    switchLoading.value[carousel.id] = false
  }
}

// 上移
const handleMoveUp = async (carousel, index) => {
  if (index === 0) return

  const currentOrder = carousel.order
  const prevCarousel = carousels.value[index - 1]
  const prevOrder = prevCarousel.order

  try {
    // 交换排序值
    await updateCarousel(carousel.id, { order: prevOrder })
    await updateCarousel(prevCarousel.id, { order: currentOrder })

    ElMessage.success('上移成功')
    await fetchCarousels()
  } catch (error) {
    console.error('上移失败:', error)
    ElMessage.error('上移失败')
  }
}

// 下移
const handleMoveDown = async (carousel, index) => {
  if (index === carousels.value.length - 1) return

  const currentOrder = carousel.order
  const nextCarousel = carousels.value[index + 1]
  const nextOrder = nextCarousel.order

  try {
    // 交换排序值
    await updateCarousel(carousel.id, { order: nextOrder })
    await updateCarousel(nextCarousel.id, { order: currentOrder })

    ElMessage.success('下移成功')
    await fetchCarousels()
  } catch (error) {
    console.error('下移失败:', error)
    ElMessage.error('下移失败')
  }
}

// 删除轮播图
const handleDelete = async (carousel) => {
  try {
    await ElMessageBox.confirm(
      `确认删除轮播图 "${carousel.title}" 吗？此操作不可恢复！`,
      '删除确认',
      {
        confirmButtonText: '确认删除',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'el-button--danger'
      }
    )

    await deleteCarousel(carousel.id)
    ElMessage.success('轮播图删除成功')
    await fetchCarousels()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除轮播图失败:', error)
      ElMessage.error(error.response?.data?.detail || error.response?.data?.error || '删除轮播图失败')
    }
  }
}

// 重置表单
const resetForm = () => {
  form.id = null
  form.title = ''
  form.image = ''
  form.link = ''
  form.position = 'home'
  form.order = 0
  form.is_active = true
  imagePreview.value = ''
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
  fetchCarousels()
})
</script>

<style scoped>
.carousels-page {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: bold;
}

.carousel-uploader {
  width: 100%;
}

.carousel-uploader :deep(.el-upload) {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: all 0.3s;
  width: 320px;
  height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.carousel-uploader :deep(.el-upload:hover) {
  border-color: #409EFF;
}

.carousel-uploader-icon {
  font-size: 28px;
  color: #8c939d;
}

.carousel-image {
  width: 320px;
  height: 120px;
  display: block;
  object-fit: cover;
}

.upload-tip {
  font-size: 12px;
  color: #999;
  margin-top: 5px;
}

.form-tip {
  font-size: 12px;
  color: #999;
  margin-top: 5px;
}

@media (max-width: 768px) {
  .carousels-page {
    padding: 10px;
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

  .carousel-uploader :deep(.el-upload),
  .carousel-image {
    width: 100%;
    height: auto;
    min-height: 120px;
  }
}
</style>
