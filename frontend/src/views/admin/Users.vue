<template>
  <div class="users-page">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>用户管理</span>
          <el-button type="primary" icon="Refresh" @click="fetchUsers" :loading="loading">
            刷新
          </el-button>
        </div>
      </template>

      <!-- 搜索和筛选区域 -->
      <div class="search-bar">
        <el-input
          v-model="searchQuery"
          placeholder="搜索用户名、姓名、手机号"
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
          v-model="userTypeFilter"
          placeholder="用户类型"
          clearable
          style="width: 150px; margin-left: 10px;"
          @change="handleSearch"
        >
          <el-option label="全部" value="" />
          <el-option label="管理员" value="admin" />
          <el-option label="运动员" value="athlete" />
          <el-option label="组织者" value="organizer" />
          <el-option label="裁判" value="referee" />
        </el-select>
      </div>

      <!-- 用户列表表格 -->
      <el-table
        :data="users"
        v-loading="loading"
        stripe
        style="width: 100%; margin-top: 20px;"
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="username" label="用户名" width="150" />
        <el-table-column label="姓名" width="120">
          <template #default="{ row }">
            {{ row.real_name || '-' }}
          </template>
        </el-table-column>
        <el-table-column label="手机号" width="130">
          <template #default="{ row }">
            {{ row.phone || '-' }}
          </template>
        </el-table-column>
        <el-table-column prop="email" label="邮箱" min-width="180" show-overflow-tooltip />
        <el-table-column label="用户类型" width="120">
          <template #default="{ row }">
            <el-tag v-if="row.user_type === 'admin'" type="danger">管理员</el-tag>
            <el-tag v-else-if="row.user_type === 'athlete'" type="success">运动员</el-tag>
            <el-tag v-else-if="row.user_type === 'organizer'" type="warning">组织者</el-tag>
            <el-tag v-else-if="row.user_type === 'referee'" type="primary">裁判</el-tag>
            <el-tag v-else type="info">未设置</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="状态" width="120">
          <template #default="{ row }">
            <el-switch
              v-model="row.is_active"
              @change="handleStatusChange(row)"
              :disabled="row.is_superuser || switchLoading[row.id]"
              active-text="启用"
              inactive-text="禁用"
            />
          </template>
        </el-table-column>
        <el-table-column label="注册时间" width="180">
          <template #default="{ row }">
            {{ formatDateTime(row.date_joined) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button
              type="primary"
              size="small"
              @click="handleViewDetail(row)"
            >
              详情
            </el-button>
            <el-button
              type="danger"
              size="small"
              @click="handleDelete(row)"
              :disabled="row.is_staff"
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

    <!-- 用户详情对话框 -->
    <el-dialog
      v-model="detailDialogVisible"
      title="用户详情"
      width="600px"
    >
      <el-descriptions v-if="currentUser" :column="2" border>
        <el-descriptions-item label="用户ID">{{ currentUser.id }}</el-descriptions-item>
        <el-descriptions-item label="用户名">{{ currentUser.username }}</el-descriptions-item>
        <el-descriptions-item label="邮箱">{{ currentUser.email || '-' }}</el-descriptions-item>
        <el-descriptions-item label="姓名">{{ currentUser.real_name || '-' }}</el-descriptions-item>
        <el-descriptions-item label="手机号">{{ currentUser.phone || '-' }}</el-descriptions-item>
        <el-descriptions-item label="性别">
          {{ getGenderText(currentUser.gender) }}
        </el-descriptions-item>
        <el-descriptions-item label="出生日期">{{ currentUser.birth_date || '-' }}</el-descriptions-item>
        <el-descriptions-item label="用户类型">
          <el-tag v-if="currentUser.user_type === 'admin'" type="danger">管理员</el-tag>
          <el-tag v-else-if="currentUser.user_type === 'athlete'" type="success">运动员</el-tag>
          <el-tag v-else-if="currentUser.user_type === 'organizer'" type="warning">组织者</el-tag>
          <el-tag v-else-if="currentUser.user_type === 'referee'" type="primary">裁判</el-tag>
          <el-tag v-else type="info">未设置</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="currentUser.is_active ? 'success' : 'danger'">
            {{ currentUser.is_active ? '活跃' : '禁用' }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="管理员">
          <el-tag :type="currentUser.is_staff ? 'success' : 'info'">
            {{ currentUser.is_staff ? '是' : '否' }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="注册时间" :span="2">
          {{ formatDateTime(currentUser.date_joined) }}
        </el-descriptions-item>
        <el-descriptions-item label="个人简介" :span="2">
          {{ currentUser.bio || '-' }}
        </el-descriptions-item>
      </el-descriptions>

      <template #footer>
        <el-button @click="detailDialogVisible = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search } from '@element-plus/icons-vue'
import { getUserList, getUserDetail, deleteUser, activateUser, deactivateUser } from '@/api/user'

// 搜索和筛选
const searchQuery = ref('')
const userTypeFilter = ref('')

// 用户列表
const users = ref([])
const loading = ref(false)
const switchLoading = ref({})

// 分页
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

// 详情对话框
const detailDialogVisible = ref(false)
const currentUser = ref(null)

// 获取用户列表
const fetchUsers = async () => {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize.value
    }

    if (searchQuery.value) {
      params.search = searchQuery.value
    }

    if (userTypeFilter.value) {
      params.user_type = userTypeFilter.value
    }

    const response = await getUserList(params)
    users.value = response.results || []
    total.value = response.count || 0
  } catch (error) {
    console.error('获取用户列表失败:', error)
    ElMessage.error('获取用户列表失败')
  } finally {
    loading.value = false
  }
}

// 搜索处理
const handleSearch = () => {
  currentPage.value = 1
  fetchUsers()
}

// 分页大小变化
const handleSizeChange = (newSize) => {
  pageSize.value = newSize
  currentPage.value = 1
  fetchUsers()
}

// 页码变化
const handlePageChange = (newPage) => {
  currentPage.value = newPage
  fetchUsers()
}

// 查看详情
const handleViewDetail = async (user) => {
  try {
    const response = await getUserDetail(user.id)
    currentUser.value = response
    detailDialogVisible.value = true
  } catch (error) {
    console.error('获取用户详情失败:', error)
    ElMessage.error('获取用户详情失败')
  }
}

// 删除用户
const handleDelete = async (user) => {
  try {
    await ElMessageBox.confirm(
      `确认删除用户 "${user.username}" 吗？此操作不可恢复！`,
      '删除确认',
      {
        confirmButtonText: '确认删除',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'el-button--danger'
      }
    )

    await deleteUser(user.id)
    ElMessage.success('用户删除成功')
    await fetchUsers()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除用户失败:', error)
      ElMessage.error(error.response?.data?.error || '删除用户失败')
    }
  }
}

// 状态切换
const handleStatusChange = async (user) => {
  switchLoading.value[user.id] = true
  try {
    if (user.is_active) {
      await activateUser(user.id)
      ElMessage.success('用户已启用')
    } else {
      await deactivateUser(user.id)
      ElMessage.success('用户已禁用')
    }
  } catch (error) {
    // 恢复原状态
    user.is_active = !user.is_active
    console.error('更新失败:', error)
    ElMessage.error(error.response?.data?.error || '更新失败')
  } finally {
    switchLoading.value[user.id] = false
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

// 获取性别文本
const getGenderText = (gender) => {
  const genderMap = {
    M: '男',
    F: '女'
  }
  return genderMap[gender] || '-'
}

onMounted(() => {
  fetchUsers()
})
</script>

<style scoped>
.users-page {
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

@media (max-width: 768px) {
  .users-page {
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
