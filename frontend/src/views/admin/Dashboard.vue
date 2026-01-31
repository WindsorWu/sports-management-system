<template>
  <div class="dashboard-container">
    <!-- 欢迎信息 -->
    <el-card class="welcome-card">
      <div class="welcome-content">
        <h2>欢迎，{{ userInfo?.username || '管理员' }}！</h2>
        <p>{{ currentTime }}</p>
      </div>
    </el-card>

    <!-- 统计卡片 -->
    <el-row :gutter="20" class="stats-row">
      <el-col :xs="12" :sm="12" :md="6" :lg="6">
        <el-card class="stat-card stat-card-1">
          <div class="stat-content">
            <div class="stat-icon">
              <el-icon :size="40"><User /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.usersCount }}</div>
              <div class="stat-label">用户总数</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :xs="12" :sm="12" :md="6" :lg="6">
        <el-card class="stat-card stat-card-2">
          <div class="stat-content">
            <div class="stat-icon">
              <el-icon :size="40"><Trophy /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.eventsCount }}</div>
              <div class="stat-label">赛事总数</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :xs="12" :sm="12" :md="6" :lg="6">
        <el-card class="stat-card stat-card-3">
          <div class="stat-content">
            <div class="stat-icon">
              <el-icon :size="40"><Document /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.registrationsCount }}</div>
              <div class="stat-label">报名总数</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :xs="12" :sm="12" :md="6" :lg="6">
        <el-card class="stat-card stat-card-4">
          <div class="stat-content">
            <div class="stat-icon">
              <el-icon :size="40"><Medal /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.resultsCount }}</div>
              <div class="stat-label">成绩总数</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 图表展示 -->
    <el-row :gutter="20" class="charts-row">
      <el-col :xs="24" :sm="24" :md="12" :lg="12">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>报名趋势图（最近7天）</span>
            </div>
          </template>
          <div ref="registrationTrendChart" style="height: 300px;"></div>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="24" :md="12" :lg="12">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>赛事状态分布</span>
            </div>
          </template>
          <div ref="eventStatusChart" style="height: 300px;"></div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 待审核报名列表 -->
    <el-card class="pending-registrations">
      <template #header>
        <div class="card-header">
          <span>待审核报名</span>
          <el-badge :value="pendingRegistrations.length" :max="99" class="badge">
            <el-button type="primary" size="small" @click="$router.push('/admin/registrations?status=pending')">
              查看全部
            </el-button>
          </el-badge>
        </div>
      </template>
      <el-table
        :data="pendingRegistrations"
        v-loading="loading"
        style="width: 100%"
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="event.name" label="赛事名称" min-width="150" />
        <el-table-column prop="user.username" label="用户" width="120" />
        <el-table-column prop="user.profile.phone" label="手机号" width="120" />
        <el-table-column prop="created_at" label="报名时间" width="180">
          <template #default="{ row }">
            {{ formatDateTime(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag type="warning">{{ getStatusText(row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button
              type="success"
              size="small"
              @click="handleApprove(row)"
              :loading="row.approving"
            >
              通过
            </el-button>
            <el-button
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
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted, computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { User, Trophy, Document, Medal } from '@element-plus/icons-vue'
import * as echarts from 'echarts'
import { getUserList } from '@/api/user'
import { getEventList } from '@/api/event'
import { getRegistrationList, approveRegistration, rejectRegistration } from '@/api/registration'
import { getResultList } from '@/api/result'

const store = useStore()
const router = useRouter()

// 获取当前用户信息
const userInfo = computed(() => store.state.user.userInfo)

// 当前时间
const currentTime = ref('')
let timeInterval = null

const updateTime = () => {
  const now = new Date()
  const options = {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    weekday: 'long',
    hour: '2-digit',
    minute: '2-digit'
  }
  currentTime.value = now.toLocaleDateString('zh-CN', options)
}

// 统计数据
const stats = reactive({
  usersCount: 0,
  eventsCount: 0,
  registrationsCount: 0,
  resultsCount: 0
})

// 待审核报名
const pendingRegistrations = ref([])
const loading = ref(false)

// 图表引用
const registrationTrendChart = ref(null)
const eventStatusChart = ref(null)
let trendChartInstance = null
let statusChartInstance = null

// 获取统计数据
const fetchStats = async () => {
  try {
    const [users, events, registrations, results] = await Promise.all([
      getUserList({ page_size: 1 }),
      getEventList({ page_size: 1 }),
      getRegistrationList({ page_size: 1 }),
      getResultList({ page_size: 1 })
    ])

    stats.usersCount = users.count || 0
    stats.eventsCount = events.count || 0
    stats.registrationsCount = registrations.count || 0
    stats.resultsCount = results.count || 0
  } catch (error) {
    console.error('获取统计数据失败:', error)
    ElMessage.error('获取统计数据失败')
  }
}

// 获取待审核报名
const fetchPendingRegistrations = async () => {
  loading.value = true
  try {
    const response = await getRegistrationList({
      status: 'pending',
      page_size: 10
    })
    pendingRegistrations.value = response.results || []
  } catch (error) {
    console.error('获取待审核报名失败:', error)
    ElMessage.error('获取待审核报名失败')
  } finally {
    loading.value = false
  }
}

// 初始化报名趋势图
const initRegistrationTrendChart = async () => {
  try {
    // 获取最近7天的数据
    const days = []
    const counts = []
    const today = new Date()

    for (let i = 6; i >= 0; i--) {
      const date = new Date(today)
      date.setDate(date.getDate() - i)
      const dateStr = date.toLocaleDateString('zh-CN', { month: 'short', day: 'numeric' })
      days.push(dateStr)

      // 模拟数据，实际应该从API获取
      // 可以通过 /api/registrations/?created_at__gte=date 来获取
      counts.push(Math.floor(Math.random() * 20) + 5)
    }

    if (!trendChartInstance) {
      trendChartInstance = echarts.init(registrationTrendChart.value)
    }

    const option = {
      tooltip: {
        trigger: 'axis'
      },
      xAxis: {
        type: 'category',
        data: days,
        boundaryGap: false
      },
      yAxis: {
        type: 'value'
      },
      series: [{
        name: '报名数量',
        type: 'line',
        smooth: true,
        data: counts,
        areaStyle: {
          color: {
            type: 'linear',
            x: 0,
            y: 0,
            x2: 0,
            y2: 1,
            colorStops: [{
              offset: 0,
              color: 'rgba(64, 158, 255, 0.5)'
            }, {
              offset: 1,
              color: 'rgba(64, 158, 255, 0.1)'
            }]
          }
        },
        itemStyle: {
          color: '#409EFF'
        }
      }]
    }

    trendChartInstance.setOption(option)
  } catch (error) {
    console.error('初始化报名趋势图失败:', error)
  }
}

// 初始化赛事状态分布图
const initEventStatusChart = async () => {
  try {
    // 获取不同状态的赛事数量
    const [draft, published, finished] = await Promise.all([
      getEventList({ status: 'draft', page_size: 1 }),
      getEventList({ status: 'published', page_size: 1 }),
      getEventList({ status: 'finished', page_size: 1 })
    ])

    const data = [
      { value: draft.count || 0, name: '草稿' },
      { value: published.count || 0, name: '已发布' },
      { value: finished.count || 0, name: '已结束' }
    ]

    if (!statusChartInstance) {
      statusChartInstance = echarts.init(eventStatusChart.value)
    }

    const option = {
      tooltip: {
        trigger: 'item',
        formatter: '{a} <br/>{b}: {c} ({d}%)'
      },
      legend: {
        orient: 'vertical',
        right: 10,
        data: ['草稿', '已发布', '已结束']
      },
      series: [{
        name: '赛事状态',
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: false,
          position: 'center'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 20,
            fontWeight: 'bold'
          }
        },
        labelLine: {
          show: false
        },
        data: data,
        color: ['#909399', '#67C23A', '#409EFF']
      }]
    }

    statusChartInstance.setOption(option)
  } catch (error) {
    console.error('初始化赛事状态分布图失败:', error)
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

// 获取状态文本
const getStatusText = (status) => {
  const statusMap = {
    pending: '待审核',
    approved: '已通过',
    rejected: '已拒绝'
  }
  return statusMap[status] || status
}

// 审核通过
const handleApprove = async (row) => {
  try {
    await ElMessageBox.confirm('确认通过该报名申请？', '提示', {
      confirmButtonText: '确认',
      cancelButtonText: '取消',
      type: 'success'
    })

    row.approving = true
    await approveRegistration(row.id)
    ElMessage.success('审核通过')
    await fetchPendingRegistrations()
    await fetchStats()
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
    const { value: remark } = await ElMessageBox.prompt('请输入拒绝原因', '拒绝审核', {
      confirmButtonText: '确认',
      cancelButtonText: '取消',
      inputPattern: /.+/,
      inputErrorMessage: '请输入拒绝原因',
      inputType: 'textarea'
    })

    row.rejecting = true
    await rejectRegistration(row.id, remark)
    ElMessage.success('已拒绝')
    await fetchPendingRegistrations()
    await fetchStats()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('拒绝失败:', error)
      ElMessage.error(error.response?.data?.error || '拒绝失败')
    }
  } finally {
    row.rejecting = false
  }
}

// 窗口大小变化时重新调整图表
const handleResize = () => {
  trendChartInstance?.resize()
  statusChartInstance?.resize()
}

onMounted(() => {
  updateTime()
  timeInterval = setInterval(updateTime, 60000) // 每分钟更新一次

  fetchStats()
  fetchPendingRegistrations()

  // 延迟初始化图表，确保DOM已渲染
  setTimeout(() => {
    initRegistrationTrendChart()
    initEventStatusChart()
  }, 100)

  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  if (timeInterval) {
    clearInterval(timeInterval)
  }

  trendChartInstance?.dispose()
  statusChartInstance?.dispose()

  window.removeEventListener('resize', handleResize)
})
</script>

<style scoped>
.dashboard-container {
  padding: 20px;
}

.welcome-card {
  margin-bottom: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.welcome-card :deep(.el-card__body) {
  padding: 30px;
}

.welcome-content h2 {
  margin: 0 0 10px 0;
  font-size: 28px;
}

.welcome-content p {
  margin: 0;
  font-size: 14px;
  opacity: 0.9;
}

.stats-row {
  margin-bottom: 20px;
}

.stat-card {
  cursor: pointer;
  transition: all 0.3s;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.stat-card-1 {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.stat-card-2 {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
}

.stat-card-3 {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  color: white;
}

.stat-card-4 {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
  color: white;
}

.stat-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px;
}

.stat-icon {
  opacity: 0.8;
}

.stat-info {
  text-align: right;
}

.stat-value {
  font-size: 32px;
  font-weight: bold;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 14px;
  opacity: 0.9;
}

.charts-row {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: bold;
}

.pending-registrations {
  margin-top: 20px;
}

.badge {
  margin-left: 10px;
}

@media (max-width: 768px) {
  .dashboard-container {
    padding: 10px;
  }

  .welcome-card :deep(.el-card__body) {
    padding: 20px;
  }

  .welcome-content h2 {
    font-size: 20px;
  }

  .stat-value {
    font-size: 24px;
  }

  .stat-label {
    font-size: 12px;
  }
}
</style>
