<template>
  <div class="carousels-page">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>轮播图管理</span>
          <el-button type="primary" @click="handleAdd">
            <el-icon><Plus /></el-icon>
            添加轮播图
          </el-button>
        </div>
      </template>
      <el-empty description="轮播图管理功能待开发" />
    </el-card>
  </div>
</template>

<script setup>
const handleAdd = () => {
  console.log('添加轮播图')
}
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
