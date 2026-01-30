<template>
  <div class="events-page">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>赛事列表</span>
          <el-input
            v-model="searchText"
            placeholder="搜索赛事"
            style="width: 300px"
            clearable
          />
        </div>
      </template>
      <el-empty description="赛事列表待开发" />
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const searchText = ref('')
</script>

<style scoped>
.events-page {
  max-width: 1200px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
