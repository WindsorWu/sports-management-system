<template>
  <div class="event-detail-page" v-loading="loading">
    <el-page-header @back="$router.back()">
      <template #content>
        <span class="page-title">赛事详情</span>
      </template>
    </el-page-header>

    <div v-if="event" class="detail-content">
      <!-- 赛事基本信息 -->
      <el-card class="info-card">
        <el-row :gutter="20">
          <el-col :xs="24" :md="12">
            <div class="event-image-wrapper">
              <img :src="event.image || defaultEventImage" class="event-image" />
              <div class="event-status-badge" :class="getStatusClass()">
                {{ getStatusText() }}
              </div>
            </div>
          </el-col>
          <el-col :xs="24" :md="12">
            <div class="event-info-box">
              <h1 class="event-name">{{ event.name }}</h1>
              <el-divider />
              <div class="info-list">
                <div class="info-item">
                  <span class="label">
                    <el-icon><Calendar /></el-icon>
                    比赛时间
                  </span>
                  <span class="value">
                    {{ formatDate(event.start_time, 'YYYY-MM-DD HH:mm') }} 至
                    {{ formatDate(event.end_time, 'YYYY-MM-DD HH:mm') }}
                  </span>
                </div>
                <div class="info-item">
                  <span class="label">
                    <el-icon><Clock /></el-icon>
                    报名截止
                  </span>
                  <span class="value">{{ formatDate(event.registration_end_time, 'YYYY-MM-DD HH:mm') }}</span>
                </div>
                <div class="info-item">
                  <span class="label">
                    <el-icon><Location /></el-icon>
                    比赛地点
                  </span>
                  <span class="value">{{ event.location }}</span>
                </div>
                <div class="info-item">
                  <span class="label">
                    <el-icon><User /></el-icon>
                    报名人数
                  </span>
                  <span class="value">{{ event.registration_count || 0 }} 人</span>
                </div>
                <div class="info-item">
                  <span class="label">
                    <el-icon><View /></el-icon>
                    浏览量
                  </span>
                  <span class="value">{{ event.click_count || 0 }} 次</span>
                </div>
              </div>
              <el-divider />
              <!-- 操作按钮 -->
              <div class="action-buttons">
                <el-button
                  type="primary"
                  size="large"
                  :disabled="!canRegister() || isRegistered"
                  @click="handleRegister"
                  :loading="registerLoading"
                >
                  <el-icon><DocumentAdd /></el-icon>
                  {{ getRegisterButtonText() }}
                </el-button>
                <el-button-group>
                  <el-button
                    :type="isLiked ? 'danger' : 'default'"
                    @click="handleLike"
                    :loading="likeLoading"
                  >
                    <el-icon><Star /></el-icon>
                    {{ isLiked ? '已点赞' : '点赞' }}
                  </el-button>
                  <el-button
                    :type="isFavorited ? 'warning' : 'default'"
                    @click="handleFavorite"
                    :loading="favoriteLoading"
                  >
                    <el-icon><Collection /></el-icon>
                    {{ isFavorited ? '已收藏' : '收藏' }}
                  </el-button>
                </el-button-group>
              </div>
            </div>
          </el-col>
        </el-row>
      </el-card>

      <!-- 详细介绍 -->
      <el-card class="description-card">
        <template #header>
          <div class="card-header">
            <el-icon><Document /></el-icon>
            <span>详细介绍</span>
          </div>
        </template>
        <div class="description-content" v-html="event.description"></div>
      </el-card>

      <!-- 已报名用户列表 -->
      <el-card class="registrations-card">
        <template #header>
          <div class="card-header">
            <el-icon><UserFilled /></el-icon>
            <span>已报名用户（{{ registrations.length }}）</span>
          </div>
        </template>
        <div v-if="registrations.length > 0" class="registrations-list">
          <el-avatar-group :max="20">
            <el-avatar
              v-for="reg in registrations"
              :key="reg.id"
              :src="reg.user.avatar"
              size="large"
            >
              {{ reg.user.username?.charAt(0) || 'U' }}
            </el-avatar>
          </el-avatar-group>
        </div>
        <el-empty v-else description="暂无报名用户" />
      </el-card>

      <!-- 评论区 -->
      <el-card class="comments-card">
        <template #header>
          <div class="card-header">
            <el-icon><ChatDotRound /></el-icon>
            <span>评论区（{{ commentTotal }}）</span>
          </div>
        </template>

        <!-- 发表评论 -->
        <div class="comment-input-wrapper">
          <el-input
            v-if="isLogin"
            v-model="commentContent"
            type="textarea"
            :rows="3"
            placeholder="请输入评论内容..."
            maxlength="500"
            show-word-limit
          />
          <div v-else class="login-tip">
            <el-text>请先 <el-link type="primary" @click="$router.push('/login')">登录</el-link> 后发表评论</el-text>
          </div>
          <div v-if="isLogin" class="comment-submit">
            <el-button type="primary" @click="handleComment" :loading="commentLoading">
              发表评论
            </el-button>
          </div>
        </div>

        <!-- 评论列表 -->
        <div v-loading="commentsLoading" class="comments-list">
          <div v-if="comments.length > 0">
            <div v-for="comment in comments" :key="comment.id" class="comment-item">
              <el-avatar :src="comment.user.avatar" :size="40">
                {{ comment.user.username?.charAt(0) || 'U' }}
              </el-avatar>
              <div class="comment-content-wrapper">
                <div class="comment-header">
                  <span class="username">{{ comment.user.username }}</span>
                  <span class="time">{{ formatDate(comment.created_at, 'YYYY-MM-DD HH:mm') }}</span>
                </div>
                <div class="comment-text">{{ comment.content }}</div>
              </div>
            </div>
          </div>
          <el-empty v-else description="暂无评论，快来发表第一条评论吧！" />
        </div>

        <!-- 评论分页 -->
        <div v-if="commentTotal > 0" class="comments-pagination">
          <el-pagination
            v-model:current-page="commentPage"
            :page-size="10"
            :total="commentTotal"
            layout="prev, pager, next"
            @current-change="handleCommentPageChange"
          />
        </div>
      </el-card>
    </div>

    <!-- 报名表单对话框 -->
    <el-dialog
      v-model="registerDialogVisible"
      title="赛事报名"
      width="600px"
      :close-on-click-modal="false"
    >
      <el-form
        ref="registerFormRef"
        :model="registerForm"
        :rules="registerRules"
        label-width="120px"
      >
        <el-form-item label="参赛者姓名" prop="participant_name">
          <el-input v-model="registerForm.participant_name" placeholder="请输入参赛者姓名" />
        </el-form-item>
        <el-form-item label="联系电话" prop="participant_phone">
          <el-input v-model="registerForm.participant_phone" placeholder="请输入联系电话" maxlength="11" />
        </el-form-item>
        <el-form-item label="身份证号" prop="participant_id_card">
          <el-input v-model="registerForm.participant_id_card" placeholder="请输入身份证号" maxlength="18" />
        </el-form-item>
        <el-form-item label="性别" prop="participant_gender">
          <el-radio-group v-model="registerForm.participant_gender">
            <el-radio label="M">男</el-radio>
            <el-radio label="F">女</el-radio>
            <el-radio label="O">其他</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="出生日期" prop="participant_birth_date">
          <el-date-picker
            v-model="registerForm.participant_birth_date"
            type="date"
            placeholder="选择出生日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
            style="width: 100%;"
          />
        </el-form-item>
        <el-form-item label="所属单位" prop="participant_organization">
          <el-input v-model="registerForm.participant_organization" placeholder="请输入所属单位（可选）" />
        </el-form-item>
        <el-form-item label="紧急联系人" prop="emergency_contact">
          <el-input v-model="registerForm.emergency_contact" placeholder="请输入紧急联系人" />
        </el-form-item>
        <el-form-item label="紧急联系电话" prop="emergency_phone">
          <el-input v-model="registerForm.emergency_phone" placeholder="请输入紧急联系电话" maxlength="11" />
        </el-form-item>
        <el-form-item label="备注" prop="remarks">
          <el-input
            v-model="registerForm.remarks"
            type="textarea"
            :rows="3"
            placeholder="请输入备注信息（可选）"
            maxlength="200"
            show-word-limit
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="registerDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitRegistration" :loading="registerLoading">
          确认报名
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useStore } from 'vuex'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Calendar,
  Clock,
  Location,
  User,
  View,
  Document,
  DocumentAdd,
  Star,
  Collection,
  UserFilled,
  ChatDotRound
} from '@element-plus/icons-vue'
import { getEventDetail, clickEvent } from '@/api/event'
import { createRegistration, getRegistrationList } from '@/api/registration'
import { like, unlike, favorite, unfavorite, getCommentList, createComment } from '@/api/interaction'
import { formatDate } from '@/utils'

const route = useRoute()
const router = useRouter()
const store = useStore()

const loading = ref(false)
const event = ref(null)
const defaultEventImage = 'https://via.placeholder.com/600x400?text=Event+Image'

// 用户状态
const isLogin = computed(() => store.getters['user/isLogin'])
const currentUser = computed(() => store.getters['user/userInfo'])

// 报名相关
const isRegistered = ref(false)
const registerLoading = ref(false)
const registrations = ref([])
const registerDialogVisible = ref(false)
const registerFormRef = ref(null)
const registerForm = ref({
  participant_name: '',
  participant_phone: '',
  participant_id_card: '',
  participant_gender: 'M',
  participant_birth_date: '',
  participant_organization: '',
  emergency_contact: '',
  emergency_phone: '',
  remarks: ''
})

// 报名表单验证规则
const registerRules = {
  participant_name: [
    { required: true, message: '请输入参赛者姓名', trigger: 'blur' }
  ],
  participant_phone: [
    { required: true, message: '请输入联系电话', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
  ],
  participant_id_card: [
    { required: true, message: '请输入身份证号', trigger: 'blur' },
    { pattern: /(^\d{15}$)|(^\d{18}$)|(^\d{17}(\d|X|x)$)/, message: '请输入正确的身份证号', trigger: 'blur' }
  ],
  participant_gender: [
    { required: true, message: '请选择性别', trigger: 'change' }
  ],
  participant_birth_date: [
    { required: true, message: '请选择出生日期', trigger: 'change' }
  ],
  emergency_contact: [
    { required: true, message: '请输入紧急联系人', trigger: 'blur' }
  ],
  emergency_phone: [
    { required: true, message: '请输入紧急联系电话', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
  ]
}

// 点赞收藏
const isLiked = ref(false)
const isFavorited = ref(false)
const likeLoading = ref(false)
const favoriteLoading = ref(false)

// 评论相关
const comments = ref([])
const commentContent = ref('')
const commentPage = ref(1)
const commentTotal = ref(0)
const commentsLoading = ref(false)
const commentLoading = ref(false)

// 获取赛事详情
const fetchEventDetail = async () => {
  loading.value = true
  try {
    const id = route.params.id
    const data = await getEventDetail(id)
    event.value = data

    // 记录点击
    await clickEvent(id).catch(() => {})

    // 检查用户状态
    if (isLogin.value) {
      checkUserStatus(data)
    }

    // 获取报名列表
    fetchRegistrations(id)
  } catch (error) {
    console.error('获取赛事详情失败:', error)
    ElMessage.error('获取赛事详情失败')
  } finally {
    loading.value = false
  }
}

// 检查用户状态（是否已报名、点赞、收藏）
const checkUserStatus = (eventData) => {
  isLiked.value = eventData.is_liked || false
  isFavorited.value = eventData.is_favorited || false
  isRegistered.value = eventData.is_registered || false
}

// 获取报名列表
const fetchRegistrations = async (eventId) => {
  try {
    const data = await getRegistrationList({ event: eventId, status: 'approved' })
    registrations.value = data.results || []
  } catch (error) {
    console.error('获取报名列表失败:', error)
  }
}

// 获取评论列表
const fetchComments = async () => {
  commentsLoading.value = true
  try {
    const id = route.params.id
    const data = await getCommentList({
      target_type: 'event',
      target_id: id,
      page: commentPage.value,
      page_size: 10
    })
    comments.value = data.results || []
    commentTotal.value = data.count || 0
  } catch (error) {
    console.error('获取评论列表失败:', error)
  } finally {
    commentsLoading.value = false
  }
}

// 判断是否可以报名
const canRegister = () => {
  if (!event.value) return false
  const now = new Date()
  const registrationEnd = new Date(event.value.registration_end_time)
  return registrationEnd > now
}

// 获取赛事状态类名
const getStatusClass = () => {
  if (!event.value) return ''
  const now = new Date()
  const registrationEnd = new Date(event.value.registration_end_time)
  const startTime = new Date(event.value.start_time)
  const endTime = new Date(event.value.end_time)

  if (now > endTime) {
    return 'status-finished'
  } else if (now >= startTime && now <= endTime) {
    return 'status-ongoing'
  } else if (now < registrationEnd) {
    return 'status-registration'
  } else {
    return 'status-waiting'
  }
}

// 获取赛事状态文本
const getStatusText = () => {
  if (!event.value) return ''
  const now = new Date()
  const registrationEnd = new Date(event.value.registration_end_time)
  const startTime = new Date(event.value.start_time)
  const endTime = new Date(event.value.end_time)

  if (now > endTime) {
    return '已结束'
  } else if (now >= startTime && now <= endTime) {
    return '进行中'
  } else if (now < registrationEnd) {
    return '报名中'
  } else {
    return '待开始'
  }
}

// 获取报名按钮文本
const getRegisterButtonText = () => {
  if (isRegistered.value) {
    return '已报名'
  }
  if (!canRegister()) {
    return '报名已截止'
  }
  return '立即报名'
}

// 处理报名
const handleRegister = async () => {
  if (!isLogin.value) {
    ElMessage.warning('请先登录')
    router.push({ path: '/login', query: { redirect: route.fullPath } })
    return
  }

  // 预填充用户信息
  if (currentUser.value) {
    registerForm.value.participant_name = currentUser.value.real_name || ''
    registerForm.value.participant_phone = currentUser.value.phone || ''
    registerForm.value.participant_id_card = currentUser.value.id_card || ''
    registerForm.value.participant_gender = currentUser.value.gender || 'M'
    registerForm.value.participant_birth_date = currentUser.value.birth_date || ''
    registerForm.value.participant_organization = currentUser.value.organization || ''
    registerForm.value.emergency_contact = currentUser.value.emergency_contact || ''
    registerForm.value.emergency_phone = currentUser.value.emergency_phone || ''
  }

  registerDialogVisible.value = true
}

// 提交报名
const submitRegistration = async () => {
  try {
    await registerFormRef.value.validate()

    registerLoading.value = true
    const data = {
      event: event.value.id,
      ...registerForm.value
    }
    await createRegistration(data)
    ElMessage.success('报名成功，等待管理员审核')
    isRegistered.value = true
    registerDialogVisible.value = false

    // 刷新报名列表
    fetchRegistrations(event.value.id)

    // 重置表单
    registerFormRef.value.resetFields()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('报名失败:', error)
      ElMessage.error(error.response?.data?.detail || error.response?.data?.error || '报名失败')
    }
  } finally {
    registerLoading.value = false
  }
}

// 处理点赞
const handleLike = async () => {
  if (!isLogin.value) {
    ElMessage.warning('请先登录')
    router.push({ path: '/login', query: { redirect: route.fullPath } })
    return
  }

  likeLoading.value = true
  try {
    if (isLiked.value) {
      await unlike('event', event.value.id)
      ElMessage.success('已取消点赞')
      isLiked.value = false
    } else {
      await like('event', event.value.id)
      ElMessage.success('点赞成功')
      isLiked.value = true
    }
  } catch (error) {
    console.error('操作失败:', error)
    ElMessage.error('操作失败')
  } finally {
    likeLoading.value = false
  }
}

// 处理收藏
const handleFavorite = async () => {
  if (!isLogin.value) {
    ElMessage.warning('请先登录')
    router.push({ path: '/login', query: { redirect: route.fullPath } })
    return
  }

  favoriteLoading.value = true
  try {
    if (isFavorited.value) {
      await unfavorite('event', event.value.id)
      ElMessage.success('已取消收藏')
      isFavorited.value = false
    } else {
      await favorite('event', event.value.id)
      ElMessage.success('收藏成功')
      isFavorited.value = true
    }
  } catch (error) {
    console.error('操作失败:', error)
    ElMessage.error('操作失败')
  } finally {
    favoriteLoading.value = false
  }
}

// 发表评论
const handleComment = async () => {
  if (!commentContent.value.trim()) {
    ElMessage.warning('请输入评论内容')
    return
  }

  commentLoading.value = true
  try {
    await createComment({
      target_type: 'event',
      target_id: event.value.id,
      content: commentContent.value
    })
    ElMessage.success('评论成功')
    commentContent.value = ''
    commentPage.value = 1
    fetchComments()
  } catch (error) {
    console.error('发表评论失败:', error)
    ElMessage.error('发表评论失败')
  } finally {
    commentLoading.value = false
  }
}

// 评论翻页
const handleCommentPageChange = (page) => {
  commentPage.value = page
  fetchComments()
}

// 页面加载时获取数据
onMounted(() => {
  fetchEventDetail()
  fetchComments()
})
</script>

<style scoped>
.event-detail-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.page-title {
  font-size: 18px;
  font-weight: 600;
}

.detail-content {
  margin-top: 20px;
}

/* 基本信息卡片 */
.info-card {
  margin-bottom: 20px;
}

.event-image-wrapper {
  position: relative;
  width: 100%;
  height: 400px;
  border-radius: 8px;
  overflow: hidden;
}

.event-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.event-status-badge {
  position: absolute;
  top: 20px;
  right: 20px;
  padding: 8px 16px;
  border-radius: 4px;
  font-size: 14px;
  font-weight: bold;
  color: #fff;
  background-color: rgba(0, 0, 0, 0.5);
}

.status-registration {
  background-color: #67C23A !important;
}

.status-ongoing {
  background-color: #409EFF !important;
}

.status-finished {
  background-color: #909399 !important;
}

.status-waiting {
  background-color: #E6A23C !important;
}

.event-info-box {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.event-name {
  margin: 0 0 10px 0;
  font-size: 28px;
  color: #303133;
}

.info-list {
  flex: 1;
}

.info-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 16px;
  font-size: 15px;
}

.info-item .label {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #606266;
  font-weight: 500;
}

.info-item .value {
  color: #303133;
  text-align: right;
}

.action-buttons {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.action-buttons .el-button {
  flex: 1;
  min-width: 120px;
}

/* 详细介绍 */
.description-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
}

.description-content {
  line-height: 1.8;
  color: #606266;
  white-space: pre-wrap;
}

/* 报名用户列表 */
.registrations-card {
  margin-bottom: 20px;
}

.registrations-list {
  padding: 10px 0;
}

/* 评论区 */
.comments-card {
  margin-bottom: 20px;
}

.comment-input-wrapper {
  margin-bottom: 20px;
}

.login-tip {
  padding: 20px;
  text-align: center;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.comment-submit {
  margin-top: 10px;
  text-align: right;
}

.comments-list {
  min-height: 200px;
}

.comment-item {
  display: flex;
  gap: 12px;
  padding: 16px 0;
  border-bottom: 1px solid #ebeef5;
}

.comment-item:last-child {
  border-bottom: none;
}

.comment-content-wrapper {
  flex: 1;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.username {
  font-weight: 600;
  color: #303133;
}

.time {
  font-size: 13px;
  color: #909399;
}

.comment-text {
  color: #606266;
  line-height: 1.6;
  word-break: break-word;
}

.comments-pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

/* 响应式布局 */
@media screen and (max-width: 768px) {
  .event-detail-page {
    padding: 10px;
  }

  .event-image-wrapper {
    height: 250px;
  }

  .event-name {
    font-size: 22px;
  }

  .info-item {
    flex-direction: column;
    gap: 6px;
  }

  .info-item .value {
    text-align: left;
  }

  .action-buttons {
    flex-direction: column;
  }

  .action-buttons .el-button {
    width: 100%;
  }

  .action-buttons .el-button-group {
    width: 100%;
    display: flex;
  }

  .action-buttons .el-button-group .el-button {
    flex: 1;
  }
}
</style>
