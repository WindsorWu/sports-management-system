# 体育赛事管理系统 - 前端

## 项目概览
采用 Vue 3 + Vite + Element Plus 构建，支持前台展示、管理后台与数据大屏（包含实时评论词云与统计）。前后端通过 JWT + REST API 协调，异步场景通过 WebSocket 词云连接。

## 技术栈
- **Vue 3（Composition API）** + **Vite**：项目骨架与构建。
- **Element Plus**：统一的组件库。
- **Vue Router**：承载前台与后台路由。
- **Vuex**：存储用户、权限、菜单与加载状态。
- **Axios**：封装请求，统一拦截 Token 失效。
- **Echarts**：用于大屏图表与词云渲染。
- **Day.js / Pinia / Sass**：辅助状态与样式。

## 运行说明
1. 进入 `frontend` 目录。
2. 安装依赖：
   ```bash
   npm install
   ```
3. 启动开发服务器：
   ```bash
   npm run dev
   ```
   访问 `http://localhost:5173`。
4. 构建打包：
   ```bash
   npm run build
   ```
   输出目录为 `dist`。

## 配置文件
- `src/api/request.js` 及相关模块统一设定 `VITE_API_BASE_URL`。
- `VITE_WEBSOCKET_PORT` 可覆盖词云 WebSocket 端口（默认 `8090`），`CommentWordCloud.vue` 会根据 `VITE_API_BASE_URL` 自动解析主机名与协议。
- 环境变量使用 `.env.development` / `.env.production` 控制。

## 实时评论词云
- 词云位于 `src/components/admin/CommentWordCloud.vue`，通过 `WordCloud` 全局脚本渲染，默认监听 `ws://<host>:8090/ws/comments/wordcloud/`。
- 前端连接后会立即收到 `wordcloud_update` 消息，如 payload 含关键词则展示；若后端返回空数组或未识别的词汇，画布继续显示“等待实时词云数据”，而状态仍提示“实时词云更新完成”，因为 WebSocket 已经接收了更新。
- 若要调试地址，可通过 `VITE_API_BASE_URL` 与 `VITE_WEBSOCKET_PORT` 配置，确保端口与 `daphne sports_backend.asgi:application --port 8090` 保持一致。

## 智能客服（MaxKB）
- 项目前端集成 MaxKB，提供智能问答与常见问题自动响应。
- 通过 Docker 启动 MaxKB 服务：
  ```bash
  docker run -d --name maxkb -p 8080:8080 fittentech/maxkb
  ```
- 完成后在 MaxKB 后台创建知识库并复制嵌入脚本，添加至 `public/index.html`，即可展示智能客服浮层。

## 目录说明
- `src/api/`：接口封装。
- `src/components/`：按页面拆分的可复用组件（包含词云、数据块、表单）。
- `src/layouts/`：`FrontendLayout.vue` 与 `AdminLayout.vue`。
- `src/store/`、`src/router/`：全局状态与路由守卫。
- `src/views/`：分前台与后台两大块，包含登录、报名、审核等页面。
- `src/assets/`：全局样式与图标资源。

## 相关文档
- `DOC.md`：架构、路由与交互逻辑说明。
