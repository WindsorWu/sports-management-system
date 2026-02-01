<template>
  <div class="referees-page">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>裁判管理</span>
        </div>
      </template>
      <el-table
        :data="referees"
        v-loading="loading"
        stripe
        style="width: 100%"
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="username" label="账号" width="160" />
        <el-table-column label="姓名" width="150">
          <template #default="{ row }">
            {{ row.real_name || '-' }}
          </template>
        </el-table-column>
        <el-table-column label="手机号" width="140">
          <template #default="{ row }">
            {{ row.phone || '-' }}
          </template>
        </el-table-column>
        <el-table-column label="可访问赛事" min-width="240">
          <template #default="{ row }">
            <template v-if="accessMap[row.id] && accessMap[row.id].length">
              <el-tag
                v-for="event in accessMap[row.id]"
                :key="`referee-${row.id}-event-${event.id}`"
                size="small"
                type="primary"
              >
                {{ event.title }}
              </el-tag>
            </template>
            <span v-else style="color: #999;">未分配赛事</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="240">
          <template #default="{ row }">
            <el-button
              type="primary"
              size="small"
              @click="openAssignDialog(row)"
            >
              分配赛事
            </el-button>
            <el-button
              type="danger"
              size="small"
              style="margin-left: 8px;"
              @click="handleOpenCancelDialog(row)"
            >
              取消分配
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog
      v-model="dialogVisible"
      title="分配裁判赛事"
      width="520px"
    >
      <div v-if="selectedReferee">
        <p style="margin-bottom: 12px; font-weight: 600;">
          {{ selectedReferee.real_name || selectedReferee.username }}（{{ selectedReferee.username }}）
        </p>
        <el-select
          v-model="selectedEventIds"
          multiple
          filterable
          collapse-tags
          placeholder="请选择赛事"
          style="width: 100%;"
        >
          <el-option
            v-for="event in events"
            :key="event.id"
            :label="`${event.name} (${event.start_time ? event.start_time.slice(0, 10) : '未排期'})`"
            :value="event.id"
          />
        </el-select>
      </div>

      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSave" :loading="assigning">
          确认保存
        </el-button>
      </template>
    </el-dialog>

    <el-dialog
      v-model="cancelDialogVisible"
      title="取消裁判赛事分配"
      width="520px"
    >
      <div v-if="selectedReferee">
        <p style="margin-bottom: 12px; font-weight: 600;">
          {{ selectedReferee.real_name || selectedReferee.username }}（{{ selectedReferee.username }}）
        </p>
        <el-select
          v-model="cancelEventIds"
          multiple
          filterable
          collapse-tags
          placeholder="请选择要取消的赛事"
          style="width: 100%;"
        >
          <el-option
            v-for="event in accessMap[selectedReferee.id]"
            :key="`cancel-${selectedReferee.id}-event-${event.id}`"
            :label="`${event.title} (${event.start_time ? event.start_time.slice(0, 10) : '未排期'})`"
            :value="event.id"
          />
        </el-select>
      </div>

      <template #footer>
        <el-button @click="cancelDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleCancelSave" :loading="cancelling">
          确认取消
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getUserList } from '@/api/user'
import { getEventList } from '@/api/event'
import { getRefereeAccessList, assignRefereeEvents, getRefereeAccessSummary } from '@/api/referee'

const referees = ref([])
const events = ref([])
const accessMap = reactive({})
const loading = ref(false)
const dialogVisible = ref(false)
const cancelDialogVisible = ref(false)
const selectedReferee = ref(null)
const selectedEventIds = ref([])
const cancelEventIds = ref([])
const assigning = ref(false)
const cancelling = ref(false)

const fetchReferees = async () => {
  loading.value = true
  try {
    const response = await getUserList({ user_type: 'referee', page_size: 200 })
    referees.value = response.results || []
  } catch (error) {
    console.error('获取裁判列表失败:', error)
    ElMessage.error('获取裁判列表失败')
  } finally {
    loading.value = false
  }
}

const fetchEvents = async () => {
  try {
    const response = await getEventList({ page_size: 1000 })
    events.value = response.results || []
  } catch (error) {
    console.error('获取赛事列表失败:', error)
    ElMessage.error('获取赛事列表失败')
  }
}

const refreshAccessMap = async () => {
  try {
    const summary = await getRefereeAccessSummary({ page_size: 1000 })
    const payload = summary || []
    const map = {}
    payload.forEach((entry) => {
      map[entry.referee] = entry.events || []
    })
    Object.keys(accessMap).forEach(key => delete accessMap[key])
    Object.assign(accessMap, map)
  } catch (error) {
    console.error('获取裁判赛事分配失败:', error)
  }
}

const openAssignDialog = async (referee) => {
  selectedReferee.value = referee
  dialogVisible.value = true
  selectedEventIds.value = []
  try {
    const response = await getRefereeAccessList({ referee: referee.id })
    selectedEventIds.value = (response || []).map(item => item.event)
  } catch (error) {
    console.error('加载裁判已有赛事失败:', error)
  }
}

const handleSave = async () => {
  if (!selectedReferee.value) return
  if (!selectedEventIds.value.length) {
    ElMessage.warning('请选择需要分配的赛事')
    return
  }
  assigning.value = true
  try {
    await assignRefereeEvents({ referee: selectedReferee.value.id, event_ids: selectedEventIds.value })
    ElMessage.success('分配成功')
    await refreshAccessMap()
    dialogVisible.value = false
  } catch (error) {
    console.error('分配失败:', error)
    ElMessage.error('分配失败，请稍后重试')
  } finally {
    assigning.value = false
  }
}

const handleOpenCancelDialog = (row) => {
  selectedReferee.value = row
  cancelDialogVisible.value = true
  cancelEventIds.value = []
}

const handleCancelSave = async () => {
  if (!selectedReferee.value) return
  if (!cancelEventIds.value.length) {
    ElMessage.warning('请选择要取消的赛事')
    return
  }
  cancelling.value = true
  try {
    const assigned = accessMap[selectedReferee.value.id] || []
    const toCancelSet = new Set(cancelEventIds.value)
    const remainingEventIds = assigned
      .filter((event) => !toCancelSet.has(event.id))
      .map((event) => event.id)
    await assignRefereeEvents({ referee: selectedReferee.value.id, event_ids: remainingEventIds })
    ElMessage.success('取消分配成功')
    await refreshAccessMap()
    cancelDialogVisible.value = false
  } catch (error) {
    console.error('取消分配失败:', error)
    ElMessage.error('取消分配失败，请稍后重试')
  } finally {
    cancelling.value = false
  }
}

onMounted(async () => {
  await Promise.all([fetchReferees(), fetchEvents(), refreshAccessMap()])
})
</script>

<style scoped>
.referees-page {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: bold;
}

.el-table .el-tag {
  margin-bottom: 4px;
}
</style>
