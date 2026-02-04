# 体育赛事管理系统 - 前端

基于 Vue 3 + Vite + Element Plus 构建的现代化项目前端，提供完整的用户体验和管理后台。

## 技术栈
- **Vue 3 (Composition API)**: 核心框架
- **Vite**: 构建与开发服务
- **Element Plus**: UI 组件库
- **Vue Router**: 路由导航
- **Vuex**: 状态管理
- **Axios**: API 请求封装
- **Echarts**: 统计图表视图
- **Sass**: CSS 预处理

## 项目特性
- **响应式布局**: 同时兼容手机端与 PC 端查看。
- **智能客服**: 通过 MaxKB 接入大模型能力，实现智能问答咨询。
- **动态权限路由**: 管理后台根据用户角色（管理员/裁判）动态显示菜单。
- **全功能编辑器**: 支持赛事信息的富文本展示。
- **实时反馈**: 集成全局消息提示与交互组件。
- **数据可视化**: 赛事报名人数分析与评论词云。

## 本地开发指南

### 1. 安装依赖
```bash
npm install
```

### 2. 启动开发环境
```bash
npm run dev
```
启动后访问 `http://localhost:5173`。

### 3. 构建打包
```bash
npm run build
```
生成的静态文件将存放在 `dist` 目录。

## 配置项
- API 请求地址在 `src/api/` 中的 `request.js` 或相关配置文件中配置。
- 环境变量可通过 `.env.development` 和 `.env.production` 进行修改。

## 目录结构说明
详见 `DOC.md`。
