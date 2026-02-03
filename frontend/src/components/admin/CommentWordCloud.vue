<template>
  <el-card class="comment-wordcloud-card">
    <template #header>
      <div class="comment-wordcloud-header">
        <span>实时评论词云</span>
        <span class="status" :class="statusLevel">{{ statusMessage }}</span>
      </div>
    </template>
    <div class="wordcloud-wrapper">
      <div ref="wordcloudRef" class="wordcloud-canvas"></div>
      <div v-if="!hasData" class="placeholder">等待实时词云数据...</div>
    </div>
    <p v-if="errorMessage" class="error-tip">{{ errorMessage }}</p>
  </el-card>
</template>

<script setup>
/* global WordCloud */
import { ref, onMounted, onBeforeUnmount } from 'vue'

const wordcloudRef = ref(null)
const statusMessage = ref('正在连接评论词云')
const statusLevel = ref('status-connecting')
const errorMessage = ref('')
const socketInstance = ref(null)
let reconnectTimer = null
const hasData = ref(false)

const resolveWsUrl = () => {
  const defaultPort = import.meta.env.VITE_WEBSOCKET_PORT || '8090'
  const defaultUrl = `ws://127.0.0.1:${defaultPort}/ws/comments/wordcloud/`
  const apiBase = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api'
  try {
    const parsed = new URL(apiBase)
    const protocol = parsed.protocol === 'https:' ? 'wss:' : 'ws:'
    const hostname = parsed.hostname
    const port = import.meta.env.VITE_WEBSOCKET_PORT || parsed.port || (protocol === 'wss:' ? '443' : '80')
    return `${protocol}//${hostname}:${port}/ws/comments/wordcloud/`
  } catch (error) {
    return defaultUrl
  }
}

const renderWordCloud = (items) => {
  const container = wordcloudRef.value
  if (!container) return
  container.innerHTML = ''
  if (typeof WordCloud === 'undefined') {
    errorMessage.value = '词云渲染脚本未加载'
    hasData.value = false
    return
  }
  if (!items?.length) {
    hasData.value = false
    return
  }
  hasData.value = true
  const list = items.map(item => [item.text || item.word, item.weight || item.count])
  WordCloud(container, {
    list,
    gridSize: 12,
    weightFactor: (size) => Math.max(15, Math.min(size * 6, 60)),
    fontFamily: 'Microsoft YaHei, SimHei, PingFang SC, Arial',
    rotateRatio: 0.15,
    backgroundColor: '#fafafa',
    color: (word, weight) => {
      const palette = ['#165dff', '#36cfc9', '#ff7d00', '#722ed1', '#f53f3f']
      return palette[weight % palette.length]
    },
  })
}

const scheduleReconnect = () => {
  clearTimeout(reconnectTimer)
  reconnectTimer = setTimeout(() => {
    initSocket()
  }, 3000)
}

const initSocket = () => {
  if (socketInstance.value) {
    socketInstance.value.close()
  }

  const ws = new WebSocket(resolveWsUrl())
  socketInstance.value = ws
  statusMessage.value = '连接中：等待后端推送'
  statusLevel.value = 'status-connecting'
  errorMessage.value = ''

  ws.onopen = () => {
    statusMessage.value = '评论词云已连接'
    statusLevel.value = 'status-success'
  }

  ws.onmessage = (event) => {
    try {
      const payload = JSON.parse(event.data)
      if (payload.type === 'wordcloud_update') {
        renderWordCloud(payload.payload)
        statusMessage.value = '实时词云更新完成'
        statusLevel.value = 'status-success'
        errorMessage.value = ''
      }
    } catch (error) {
      errorMessage.value = '解析词云数据失败'
    }
  }

  ws.onclose = () => {
    statusMessage.value = '连接已断开，3秒后重连'
    statusLevel.value = 'status-warning'
    scheduleReconnect()
  }

  ws.onerror = () => {
    errorMessage.value = '评论词云连接异常'
    statusLevel.value = 'status-error'
  }
}

const destroySocket = () => {
  clearTimeout(reconnectTimer)
  if (socketInstance.value) {
    socketInstance.value.close()
    socketInstance.value = null
  }
}

onMounted(() => initSocket())
onBeforeUnmount(() => destroySocket())
</script>

<style scoped>
.comment-wordcloud-card {
  min-height: 360px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.comment-wordcloud-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: bold;
}
.status {
  font-size: 12px;
  padding: 2px 10px;
  border-radius: 999px;
}
.status-connecting {
  background: #f0f9ff;
  color: #1890ff;
}
.status-success {
  background: #f6ffed;
  color: #52c41a;
}
.status-warning {
  background: #fff7e6;
  color: #fa8c16;
}
.status-error {
  background: #fff1f0;
  color: #f5222d;
}
.subtitle {
  margin: 0;
  font-size: 12px;
  color: #888;
}
.wordcloud-wrapper {
  flex: 1;
  border: 1px dashed #dcdfe6;
  border-radius: 4px;
  position: relative;
  overflow: hidden;
  min-height: 260px;
}
.wordcloud-canvas {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
}
.placeholder {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #bbb;
  font-size: 14px;
}
.error-tip {
  margin: 0;
  font-size: 12px;
  color: #f56c6c;
}
</style>
