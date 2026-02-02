<template>
  <div class="dashboard-container">
    <!-- 娆㈣繋淇℃伅 -->
    <el-card class="welcome-card">
      <div class="welcome-content">
        <h2>娆㈣繋锛寋{ userInfo?.username || '绠＄悊鍛? }}锛?/h2>
        <p>{{ currentTime }}</p>
      </div>
    </el-card>

    <!-- 缁熻鍗＄墖 -->
    <el-row :gutter="20" class="stats-row">
      <el-col :xs="12" :sm="12" :md="6" :lg="6">
        <el-card class="stat-card stat-card-1">
          <div class="stat-content">
            <div class="stat-icon">
              <el-icon :size="40"><User /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.usersCount }}</div>
              <div class="stat-label">鐢ㄦ埛鎬绘暟</div>
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
              <div class="stat-label">璧涗簨鎬绘暟</div>
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
              <div class="stat-label">鎶ュ悕鎬绘暟</div>
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
              <div class="stat-label">鎴愮哗鎬绘暟</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 鍥捐〃灞曠ず -->
    <el-row :gutter="20" class="charts-row">
      <el-col :xs="24" :sm="24" :md="12" :lg="12">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>鎶ュ悕瓒嬪娍鍥撅紙鏈€杩?澶╋級</span>
            </div>
          </template>
          <div ref="registrationTrendChart" style="height: 300px;"></div>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="24" :md="12" :lg="12">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>璧涗簨鐘舵€佸垎甯?/span>
            </div>
          </template>
          <div ref="eventStatusChart" style="height: 300px;"></div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 寰呭鏍告姤鍚嶅垪琛?-->
    <el-card class="pending-registrations">
      <template #header>
        <div class="card-header">
          <span>寰呭鏍告姤鍚?/span>
          <el-badge :value="pendingRegistrations.length" :max="99" class="badge">
            <el-button type="primary" size="small" @click="$router.push('/admin/registrations?status=pending')">
              鏌ョ湅鍏ㄩ儴
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
        <el-table-column prop="event.name" label="璧涗簨鍚嶇О" min-width="150" />
        <el-table-column prop="user.username" label="鐢ㄦ埛" width="120" />
        <el-table-column prop="user.profile.phone" label="鎵嬫満鍙? width="120" />
        <el-table-column prop="created_at" label="鎶ュ悕鏃堕棿" width="180">
          <template #default="{ row }">
            {{ formatDateTime(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="鐘舵€? width="100">
          <template #default="{ row }">
            <el-tag type="warning">{{ getStatusText(row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="鎿嶄綔" width="200" fixed="right">
          <template #default="{ row }">
            <el-button
              type="success"
              size="small"
              @click="handleApprove(row)"
              :loading="row.approving"
            >
              閫氳繃
            </el-button>
            <el-button
              type="danger"
              size="small"
              @click="handleReject(row)"
              :loading="row.rejecting"
            >
              鎷掔粷
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted, computed, nextTick } from 'vue'
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

// 鑾峰彇褰撳墠鐢ㄦ埛淇℃伅
const userInfo = computed(() => store.state.user.userInfo)

// 褰撳墠鏃堕棿
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

// 缁熻鏁版嵁
const stats = reactive({
  usersCount: 0,
  eventsCount: 0,
  registrationsCount: 0,
  resultsCount: 0
})

// 寰呭鏍告姤鍚?const pendingRegistrations = ref([])
const loading = ref(false)

// 鍥捐〃寮曠敤
const registrationTrendChart = ref(null)
const eventStatusChart = ref(null)
let trendChartInstance = null
let statusChartInstance = null

// 鑾峰彇缁熻鏁版嵁
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
    console.error('鑾峰彇缁熻鏁版嵁澶辫触:', error)
    ElMessage.error('鑾峰彇缁熻鏁版嵁澶辫触')
  }
}

// 鑾峰彇寰呭鏍告姤鍚?const fetchPendingRegistrations = async () => {
  loading.value = true
  try {
    const response = await getRegistrationList({
      status: 'pending',
      page_size: 10
    })
    pendingRegistrations.value = response.results || []
  } catch (error) {
    console.error('鑾峰彇寰呭鏍告姤鍚嶅け璐?', error)
    ElMessage.error('鑾峰彇寰呭鏍告姤鍚嶅け璐?)
  } finally {
    loading.value = false
  }
}

// 鍒濆鍖栨姤鍚嶈秼鍔垮浘
const initRegistrationTrendChart = async () => {
  try {
    // 鑾峰彇鏈€杩?澶╃殑鏁版嵁
    const days = []
    const counts = []
    const today = new Date()

    for (let i = 6; i >= 0; i--) {
      const date = new Date(today)
      date.setDate(date.getDate() - i)
      const dateStr = date.toLocaleDateString('zh-CN', { month: 'short', day: 'numeric' })
      days.push(dateStr)

      // 妯℃嫙鏁版嵁锛屽疄闄呭簲璇ヤ粠API鑾峰彇
      // 鍙互閫氳繃 /api/registrations/?created_at__gte=date 鏉ヨ幏鍙?      counts.push(Math.floor(Math.random() * 20) + 5)
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
        name: '鎶ュ悕鏁伴噺',
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
    console.error('鍒濆鍖栨姤鍚嶈秼鍔垮浘澶辫触:', error)
  }
}

// 鍒濆鍖栬禌浜嬬姸鎬佸垎甯冨浘
const initEventStatusChart = async () => {
  try {
    // 鑾峰彇涓嶅悓鐘舵€佺殑璧涗簨鏁伴噺
    const [draft, published, finished] = await Promise.all([
      getEventList({ status: 'draft', page_size: 1 }),
      getEventList({ status: 'published', page_size: 1 }),
      getEventList({ status: 'finished', page_size: 1 })
    ])

    const data = [
      { value: draft.count || 0, name: '鑽夌' },
      { value: published.count || 0, name: '宸插彂甯? },
      { value: finished.count || 0, name: '宸茬粨鏉? }
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
        data: ['鑽夌', '宸插彂甯?, '宸茬粨鏉?]
      },
      series: [{
        name: '璧涗簨鐘舵€?,
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
    console.error('鍒濆鍖栬禌浜嬬姸鎬佸垎甯冨浘澶辫触:', error)
  }
}

// 鏍煎紡鍖栨棩鏈熸椂闂?const formatDateTime = (dateStr) => {
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

// 鑾峰彇鐘舵€佹枃鏈?const getStatusText = (status) => {
  const statusMap = {
    pending: '寰呭鏍?,
    approved: '宸查€氳繃',
    rejected: '宸叉嫆缁?
  }
  return statusMap[status] || status
}

// 瀹℃牳閫氳繃
const handleApprove = async (row) => {
  try {
    await ElMessageBox.confirm('纭閫氳繃璇ユ姤鍚嶇敵璇凤紵', '鎻愮ず', {
      confirmButtonText: '纭',
      cancelButtonText: '鍙栨秷',
      type: 'success'
    })

    row.approving = true
    await approveRegistration(row.id)
    ElMessage.success('瀹℃牳閫氳繃')
    await fetchPendingRegistrations()
    await fetchStats()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('瀹℃牳澶辫触:', error)
      ElMessage.error(error.response?.data?.error || '瀹℃牳澶辫触')
    }
  } finally {
    row.approving = false
  }
}

// 瀹℃牳鎷掔粷
const handleReject = async (row) => {
  try {
    const { value: remark } = await ElMessageBox.prompt('璇疯緭鍏ユ嫆缁濆師鍥?, '鎷掔粷瀹℃牳', {
      confirmButtonText: '纭',
      cancelButtonText: '鍙栨秷',
      inputPattern: /.+/,
      inputErrorMessage: '璇疯緭鍏ユ嫆缁濆師鍥?,
      inputType: 'textarea'
    })

    row.rejecting = true
    await rejectRegistration(row.id, remark)
    ElMessage.success('宸叉嫆缁?)
    await fetchPendingRegistrations()
    await fetchStats()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('鎷掔粷澶辫触:', error)
      ElMessage.error(error.response?.data?.error || '鎷掔粷澶辫触')
    }
  } finally {
    row.rejecting = false
  }
}

// 绐楀彛澶у皬鍙樺寲鏃堕噸鏂拌皟鏁村浘琛?const handleResize = () => {
  trendChartInstance?.resize()
  statusChartInstance?.resize()
}

onMounted(async () => {
  updateTime()
  timeInterval = setInterval(updateTime, 60000) // 姣忓垎閽熸洿鏂颁竴娆?
  fetchStats()
  fetchPendingRegistrations()

  // 绛夊緟 DOM 瀹屽叏娓叉煋鍐嶅垵濮嬪寲鍥捐〃
  await nextTick()
  initRegistrationTrendChart()
  initEventStatusChart()

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
