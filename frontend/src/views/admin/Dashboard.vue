<template>
  <div class="dashboard">
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card shadow="hover">
          <el-statistic title="总用户数" :value="0">
            <template #prefix>
              <el-icon><User /></el-icon>
            </template>
          </el-statistic>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <el-statistic title="赛事数量" :value="0">
            <template #prefix>
              <el-icon><Trophy /></el-icon>
            </template>
          </el-statistic>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <el-statistic title="报名数量" :value="0">
            <template #prefix>
              <el-icon><Document /></el-icon>
            </template>
          </el-statistic>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover">
          <el-statistic title="公告数量" :value="0">
            <template #prefix>
              <el-icon><Bell /></el-icon>
            </template>
          </el-statistic>
        </el-card>
      </el-col>
    </el-row>
    <el-card style="margin-top: 20px;">
      <el-empty description="数据统计功能待开发" />
    </el-card>
  </div>
</template>

<script setup>
</script>

<style scoped>
.dashboard {
  padding: 20px;
}
</style>
