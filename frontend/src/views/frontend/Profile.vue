<template>
  <div class="profile-page">
    <!-- 个人信息卡片 -->
    <el-card class="user-info-card" shadow="hover">
      <div class="user-info">
        <div class="avatar-section">
          <el-avatar :size="100" :src="userInfo.avatar" class="user-avatar">
            {{ userInfo.username?.charAt(0).toUpperCase() }}
          </el-avatar>
        </div>
        <div class="info-section">
          <h2 class="username">{{ userInfo.username }}</h2>
          <div class="user-details">
            <div class="detail-item">
              <el-icon><User /></el-icon>
              <span>真实姓名：{{ userInfo.real_name || '未设置' }}</span>
            </div>
            <div class="detail-item">
              <el-icon><Phone /></el-icon>
              <span>手机号：{{ userInfo.phone || '未设置' }}</span>
            </div>
            <div class="detail-item">
              <el-icon><Message /></el-icon>
              <span>邮箱：{{ userInfo.email || '未设置' }}</span>
            </div>
          </div>
        </div>
        <div class="action-section">
          <el-button type="primary" @click="showEditDialog = true">
            <el-icon><Edit /></el-icon> 编辑资料
          </el-button>
          <el-button @click="showPasswordDialog = true">
            <el-icon><Lock /></el-icon> 修改密码
          </el-button>
        </div>
      </div>
    </el-card>

    <!-- Tab标签页 -->
    <el-card class="content-card" shadow="hover">
      <el-tabs v-model="activeTab" @tab-change="handleTabChange">
        <!-- 我的报名 -->
        <el-tab-pane label="我的报名" name="registrations">
          <div v-loading="loading.registrations">
            <el-table
              :data="registrations"
              style="width: 100%"
              :empty-text="'暂无报名记录'"
            >
              <el-table-column label="赛事名称" min-width="200">
                <template #default="{ row }">
                  {{ row.event_title || '-' }}
                </template>
              </el-table-column>
              <el-table-column label="参赛者姓名" width="120">
                <template #default="{ row }">
                  {{ row.participant_name || '-' }}
                </template>
              </el-table-column>
              <el-table-column label="报名时间" width="180">
                <template #default="{ row }">
                  {{ formatDate(row.created_at, 'YYYY-MM-DD HH:mm') }}
                </template>
              </el-table-column>
              <el-table-column label="审核状态" width="120">
                <template #default="{ row }">
                  <el-tag
                    :type="getStatusType(row.status)"
                    effect="dark"
                  >
                    {{ getStatusText(row.status) }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column label="操作" width="180" fixed="right">
                <template #default="{ row }">
                  <el-button
                    link
                    type="primary"
                    @click="goToEventDetail(row.event)"
                  >
                    查看赛事
                  </el-button>
                  <el-button
                    v-if="row.status === 'pending'"
                    link
                    type="danger"
                    @click="handleCancelRegistration(row.id)"
                  >
                    取消报名
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-tab-pane>

        <!-- 我的收藏 -->
        <el-tab-pane label="我的收藏" name="favorites">
          <div v-loading="loading.favorites">
            <div v-if="favorites.length === 0" class="empty-container">
              <el-empty description="暂无收藏" />
            </div>
            <div v-else class="favorites-grid">
              <el-card
                v-for="item in favorites"
                :key="item.id"
                class="favorite-card"
                shadow="hover"
                @click="goToEventDetail(item.target_id)"
              >
                <img
                  :src="item.event_image || '/default-event.jpg'"
                  class="event-image"
                  @error="handleImageError"
                />
                <div class="favorite-content">
                  <h3 class="event-title">{{ item.event_name }}</h3>
                  <div class="event-info">
                    <el-tag size="small">{{ item.event_type }}</el-tag>
                    <span class="event-time">
                      {{ formatDate(item.event_start_time, 'YYYY-MM-DD') }}
                    </span>
                  </div>
                  <div class="favorite-time">
                    收藏于 {{ formatDate(item.created_at, 'YYYY-MM-DD') }}
                  </div>
                </div>
              </el-card>
            </div>
          </div>
        </el-tab-pane>

        <!-- 我的成绩 -->
        <el-tab-pane label="我的成绩" name="results">
          <div v-loading="loading.results">
            <el-table
              :data="results"
              style="width: 100%"
              :empty-text="'暂无成绩记录'"
            >
              <el-table-column label="赛事名称" min-width="200">
                <template #default="{ row }">
                  {{ row.event_title || '-' }}
                </template>
              </el-table-column>
              <el-table-column label="轮次" width="100">
                <template #default="{ row }">
                  <el-tag v-if="row.round_type === 'final'" type="danger">决赛</el-tag>
                  <el-tag v-else-if="row.round_type === 'semifinal'" type="warning">半决赛</el-tag>
                  <el-tag v-else-if="row.round_type === 'preliminary'" type="info">初赛</el-tag>
                  <el-tag v-else>-</el-tag>
                </template>
              </el-table-column>
              <el-table-column label="成绩" width="120">
                <template #default="{ row }">
                  <span class="score-text">{{ row.score }}</span>
                </template>
              </el-table-column>
              <el-table-column label="排名" width="100">
                <template #default="{ row }">
                  <el-tag
                    v-if="row.rank"
                    :type="getRankingType(row.rank)"
                    effect="dark"
                  >
                    第{{ row.rank }}名
                  </el-tag>
                  <span v-else>-</span>
                </template>
              </el-table-column>
              <el-table-column label="奖项" width="120">
                <template #default="{ row }">
                  {{ row.award || '-' }}
                </template>
              </el-table-column>
              <el-table-column label="发布时间" width="180">
                <template #default="{ row }">
                  {{ formatDate(row.created_at, 'YYYY-MM-DD HH:mm') }}
                </template>
              </el-table-column>
              <el-table-column label="操作" width="120" fixed="right">
                <template #default="{ row }">
                  <el-button
                    link
                    type="primary"
                    @click="goToEventDetail(row.event)"
                  >
                    查看赛事
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-tab-pane>
      </el-tabs>
    </el-card>

    <!-- 编辑个人信息对话框 -->
    <el-dialog
      v-model="showEditDialog"
      title="编辑个人信息"
      width="500px"
      :close-on-click-modal="false"
    >
      <el-form
        ref="editFormRef"
        :model="editForm"
        :rules="editRules"
        label-width="80px"
      >
        <el-form-item label="用户名" prop="username">
          <el-input v-model="editForm.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="手机号" prop="phone">
          <el-input v-model="editForm.phone" placeholder="请输入手机号" />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="editForm.email" placeholder="请输入邮箱" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showEditDialog = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="handleUpdateInfo">
          保存
        </el-button>
      </template>
    </el-dialog>

    <!-- 修改密码对话框 -->
    <el-dialog
      v-model="showPasswordDialog"
      title="修改密码"
      width="500px"
      :close-on-click-modal="false"
    >
      <el-form
        ref="passwordFormRef"
        :model="passwordForm"
        :rules="passwordRules"
        label-width="100px"
      >
        <el-form-item label="原密码" prop="old_password">
          <el-input
            v-model="passwordForm.old_password"
            type="password"
            placeholder="请输入原密码"
            show-password
          />
        </el-form-item>
        <el-form-item label="新密码" prop="new_password">
          <el-input
            v-model="passwordForm.new_password"
            type="password"
            placeholder="请输入新密码"
            show-password
          />
        </el-form-item>
        <el-form-item label="确认密码" prop="new_password_confirm">
          <el-input
            v-model="passwordForm.new_password_confirm"
            type="password"
            placeholder="请再次输入新密码"
            show-password
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showPasswordDialog = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="handleChangePassword">
          确认修改
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { User, Phone, Message, Edit, Lock } from '@element-plus/icons-vue'
import { getUserInfo, updateUserInfo, changePassword } from '@/api/user'
import { getMyRegistrations, cancelRegistration } from '@/api/registration'
import { getMyFavorites } from '@/api/interaction'
import { getMyResults } from '@/api/result'
import { formatDate, validateEmail, validatePhone } from '@/utils'

const store = useStore()
const router = useRouter()

// 用户信息
const userInfo = computed(() => store.state.user.userInfo)

// Tab切换
const activeTab = ref('registrations')

// 加载状态
const loading = reactive({
  registrations: false,
  favorites: false,
  results: false
})

// 数据列表
const registrations = ref([])
const favorites = ref([])
const results = ref([])

// 对话框显示状态
const showEditDialog = ref(false)
const showPasswordDialog = ref(false)
const submitting = ref(false)

// 编辑个人信息表单
const editFormRef = ref(null)
const editForm = reactive({
  username: '',
  phone: '',
  email: ''
})

// 验证规则
const validateUsernameRule = (rule, value, callback) => {
  if (!value) {
    callback(new Error('请输入用户名'))
  } else {
    callback()
  }
}

const validatePhoneRule = (rule, value, callback) => {
  if (value && !validatePhone(value)) {
    callback(new Error('请输入正确的手机号'))
  } else {
    callback()
  }
}

const validateEmailRule = (rule, value, callback) => {
  if (value && !validateEmail(value)) {
    callback(new Error('请输入正确的邮箱地址'))
  } else {
    callback()
  }
}

const editRules = {
  username: [{ validator: validateUsernameRule, trigger: 'blur' }],
  phone: [{ validator: validatePhoneRule, trigger: 'blur' }],
  email: [{ validator: validateEmailRule, trigger: 'blur' }]
}

// 修改密码表单
const passwordFormRef = ref(null)
const passwordForm = reactive({
  old_password: '',
  new_password: '',
  new_password_confirm: ''
})

const validatePasswordConfirm = (rule, value, callback) => {
  if (value !== passwordForm.new_password) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

const passwordRules = {
  old_password: [
    { required: true, message: '请输入原密码', trigger: 'blur' }
  ],
  new_password: [
    { required: true, message: '请输入新密码', trigger: 'blur' }
  ],
  new_password_confirm: [
    { required: true, message: '请再次输入新密码', trigger: 'blur' },
    { validator: validatePasswordConfirm, trigger: 'blur' }
  ]
}

// Tab切换处理
const handleTabChange = (tabName) => {
  if (tabName === 'registrations' && registrations.value.length === 0) {
    loadRegistrations()
  } else if (tabName === 'favorites' && favorites.value.length === 0) {
    loadFavorites()
  } else if (tabName === 'results' && results.value.length === 0) {
    loadResults()
  }
}

// 加载我的报名
const loadRegistrations = async () => {
  loading.registrations = true
  try {
    const data = await getMyRegistrations()
    registrations.value = data
  } catch (error) {
    ElMessage.error(error.message || '加载报名记录失败')
  } finally {
    loading.registrations = false
  }
}

// 加载我的收藏
const loadFavorites = async () => {
  loading.favorites = true
  try {
    const data = await getMyFavorites()
    favorites.value = data.results || data || []
  } catch (error) {
    ElMessage.error(error.message || '加载收藏列表失败')
  } finally {
    loading.favorites = false
  }
}

// 加载我的成绩
const loadResults = async () => {
  loading.results = true
  try {
    const data = await getMyResults()
    results.value = data
  } catch (error) {
    ElMessage.error(error.message || '加载成绩记录失败')
  } finally {
    loading.results = false
  }
}

// 获取报名状态类型
const getStatusType = (status) => {
  const typeMap = {
    pending: 'warning',
    approved: 'success',
    rejected: 'danger',
    cancelled: 'info'
  }
  return typeMap[status] || 'info'
}

// 获取报名状态文本
const getStatusText = (status) => {
  const textMap = {
    pending: '待审核',
    approved: '已通过',
    rejected: '已拒绝',
    cancelled: '已取消'
  }
  return textMap[status] || status
}

// 获取排名标签类型
const getRankingType = (rank) => {
  if (rank === 1) return 'danger'
  if (rank === 2) return 'warning'
  if (rank === 3) return 'success'
  return 'info'
}

// 取消报名
const handleCancelRegistration = (id) => {
  ElMessageBox.confirm('确定要取消这个报名吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await cancelRegistration(id)
      ElMessage.success('取消报名成功')
      loadRegistrations()
    } catch (error) {
      ElMessage.error(error.message || '取消报名失败')
    }
  }).catch(() => {})
}

// 跳转到赛事详情
const goToEventDetail = (eventId) => {
  router.push(`/events/${eventId}`)
}

// 更新个人信息
const handleUpdateInfo = async () => {
  try {
    await editFormRef.value.validate()
    submitting.value = true

    const data = await updateUserInfo(editForm)

    // 更新Vuex中的用户信息
    await store.dispatch('user/getUserInfo')

    ElMessage.success('更新个人信息成功')
    showEditDialog.value = false
  } catch (error) {
    if (error !== false) { // 表单验证失败时返回false
      ElMessage.error(error.message || '更新个人信息失败')
    }
  } finally {
    submitting.value = false
  }
}

// 修改密码
const handleChangePassword = async () => {
  try {
    await passwordFormRef.value.validate()
    submitting.value = true

    const payload = {
      old_password: passwordForm.old_password,
      new_password: passwordForm.new_password,
      new_password_confirm: passwordForm.new_password_confirm
    }
    await changePassword(payload)

    ElMessage.success('修改密码成功，请重新登录')
    showPasswordDialog.value = false

    // 退出登录
    setTimeout(() => {
      store.dispatch('user/logout')
      router.push('/login')
    }, 1500)
  } catch (error) {
    if (error !== false) {
      const message = error.response?.data?.detail
        || error.response?.data?.message
        || Object.values(error.response?.data || {}).flat().join(', ')
        || error.message
        || '修改密码失败'
      ElMessage.error(message)
    }
  } finally {
    submitting.value = false
  }
}

// 图片加载失败处理
const handleImageError = (e) => {
  e.target.src = '/default-event.jpg'
}

// 初始化
onMounted(() => {
  // 填充编辑表单
  editForm.username = userInfo.value.username || ''
  editForm.phone = userInfo.value.phone || ''
  editForm.email = userInfo.value.email || ''

  // 加载默认tab数据
  loadRegistrations()
})
</script>

<style scoped>
.profile-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

/* 用户信息卡片 */
.user-info-card {
  margin-bottom: 20px;
  border-radius: 8px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 30px;
}

.avatar-section {
  flex-shrink: 0;
}

.user-avatar {
  font-size: 36px;
  font-weight: bold;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.info-section {
  flex: 1;
}

.username {
  margin: 0 0 16px 0;
  font-size: 24px;
  color: #303133;
}

.user-details {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #606266;
  font-size: 14px;
}

.detail-item .el-icon {
  color: #909399;
}

.action-section {
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

/* 内容卡片 */
.content-card {
  border-radius: 8px;
}

/* 收藏网格 */
.favorites-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
  margin-top: 16px;
}

.favorite-card {
  cursor: pointer;
  transition: all 0.3s;
  border-radius: 8px;
  overflow: hidden;
}

.favorite-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.event-image {
  width: 100%;
  height: 160px;
  object-fit: cover;
  display: block;
}

.favorite-content {
  padding: 16px;
}

.event-title {
  margin: 0 0 12px 0;
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.event-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.event-time {
  font-size: 13px;
  color: #909399;
}

.favorite-time {
  font-size: 12px;
  color: #C0C4CC;
}

.empty-container {
  padding: 40px 0;
}

/* 成绩高亮 */
.score-text {
  font-weight: 600;
  color: #409eff;
  font-size: 15px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .user-info {
    flex-direction: column;
    text-align: center;
  }

  .user-details {
    align-items: center;
  }

  .action-section {
    width: 100%;
  }

  .action-section .el-button {
    width: 100%;
  }

  .favorites-grid {
    grid-template-columns: 1fr;
  }
}
</style>
