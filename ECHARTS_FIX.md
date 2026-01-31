# ECharts依赖缺失问题修复

## 问题描述

**错误信息**:
```
Failed to resolve import "echarts" from "src/views/admin/Dashboard.vue"
```

**发生场景**: 访问管理后台Dashboard页面时编译失败

## 修复方案

安装echarts包：
```bash
cd frontend
npm install echarts
```

## 操作步骤

1. **重启前端服务器**（重要！）
   - 按 Ctrl+C 停止当前服务器
   - 运行 `npm run dev` 重新启动

2. **清除localStorage**
   ```javascript
   localStorage.clear()
   ```

3. **重新登录**
   - 用户名: admin
   - 密码: admin

4. **访问管理后台**
   ```
   http://localhost:5173/admin
   ```

## 预期结果
- ✅ Dashboard页面正常加载
- ✅ 图表正常显示

---

**状态**: ✅ 已完成（echarts已安装）
**版本**: v1.0.9
