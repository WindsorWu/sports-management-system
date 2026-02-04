# 前端项目开发文档

## 1. 架构设计

本项目采用前后端分离架构，前端作为独立 SPA（单页应用）运行。

### 1.1 核心目录结构
- `src/api/`: 所有的 API 请求函数，按模块划分（如 `user.js`, `event.js`）。
- `src/assets/`: 存放静态资源如图片、图标和全局样式。
- `src/components/`: 可复用的公共组件。
- `src/layouts/`: 页面布局组件
    - `FrontendLayout.vue`: 普通用户前台门户布局。
    - `AdminLayout.vue`: 后台管理系统侧边栏布局。
- `src/router/`: 路由配置，包含路由守卫（登录拦截、角色校验）。
- `src/store/`: Vuex 状态管理，存储用户信息、全局变量等。
- `src/views/`: 业务页面
    - `frontend/`: 首页、赛事列表、详情、个人中心。
    - `admin/`: 管理端的各种管理模块页面。
    - `Login.vue`, `Register.vue`: 认证页面。
- `src/utils/`: 工具函数库（验证、日期格式化、Token 存储）。

## 2. 路由逻辑

### 2.1 路由守卫 (`router/index.js`)
- **登录状态检查**: 访问标记了 `requiresAuth: true` 的路由时，会检查 localStorage/Cookie 是否存在 Token。
- **角色校验**: 访问 `/admin` 及其子路径时，会根据用户信息中的 `user_type` 和 `is_staff` 判定是否有权访问。

## 3. 状态管理 (Vuex)

- `user`: 维护当前用户的基本信息（Token, 用户名, 角色, ID）。
- `app`: 全局状态控制（侧边栏展开折叠、加载状态）。

## 4. 组件规范

- 使用 Vue 3 `<script setup>` 语法糖。
- 组件命名遵循 PascalCase 规范。
- UI 组件优先使用 Element Plus。

## 5. 主要页面说明

### 5.1 前台 (User-Facing)
- 首页: 轮播图显示、推荐赛事、最新公告。
- 赛事详情: 展示详细描述、规则、地点，支持点赞、收藏及发表评论。
- 报名弹窗: 在赛事详情页点击报名，填写必要信息。

### 5.2 后台 (Admin-Facing)
- 数据大屏 (Dashboard): 统计关键数据。
- 成绩录入: 支持手动编辑单条成绩，也支持通过 Excel 文件一键上传整场赛事的成绩。

## 6. 智能客服集成

项目通过在 `public/index.html` (或 `index.html`) 中引入 MaxKB 提供的嵌入式脚本实现智能客服功能。
- **技术实现**: 使用脚本注入方式加载 MaxKB 聊天应用。
- **配置**: 如需修改机器人配置或 Token，请在 `index.html` 的 `<script>` 标签中更新 URL。

## 7. 与后端交互

- API 请求基础路径统一配置，使用拦截器处理 401 (未登录) 状态并自动清除失效 Token。
- 采用 JWT 认证，Headers 格式: `Authorization: Bearer <token>`。
