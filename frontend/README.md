# 体育赛事管理系统 - 前端

基于 Vue 3 + Vite + Element Plus 构建的现代化体育赛事管理系统前端应用。

## 技术栈

- **框架**: Vue 3.3+ (Composition API)
- **构建工具**: Vite 5.0+
- **路由**: Vue Router 4
- **状态管理**: Vuex 4
- **UI框架**: Element Plus 2.4+
- **HTTP客户端**: Axios 1.6+
- **其他**: js-cookie, dayjs

## 项目结构

```
frontend/
├── public/                # 静态资源
├── src/
│   ├── api/              # API接口封装
│   │   ├── user.js       # 用户相关接口
│   │   ├── event.js      # 赛事相关接口
│   │   ├── registration.js # 报名相关接口
│   │   ├── result.js     # 成绩相关接口
│   │   ├── announcement.js # 公告相关接口
│   │   ├── interaction.js  # 互动相关接口
│   │   ├── carousel.js   # 轮播图相关接口
│   │   ├── feedback.js   # 反馈相关接口
│   │   └── common.js     # 通用接口
│   ├── assets/           # 资源文件
│   ├── components/       # 公共组件
│   ├── layouts/          # 布局组件
│   │   ├── FrontendLayout.vue  # 前台布局
│   │   └── AdminLayout.vue     # 后台布局
│   ├── router/           # 路由配置
│   │   └── index.js
│   ├── store/            # Vuex状态管理
│   │   ├── index.js
│   │   └── modules/
│   │       ├── user.js   # 用户模块
│   │       └── app.js    # 应用模块
│   ├── utils/            # 工具函数
│   │   ├── request.js    # Axios封装
│   │   ├── auth.js       # Token管理
│   │   └── index.js      # 通用工具
│   ├── views/            # 页面组件
│   │   ├── frontend/     # 前台页面
│   │   │   ├── Home.vue
│   │   │   ├── Events.vue
│   │   │   ├── EventDetail.vue
│   │   │   ├── Announcements.vue
│   │   │   └── Profile.vue
│   │   ├── admin/        # 后台管理页面
│   │   │   ├── Dashboard.vue
│   │   │   ├── Users.vue
│   │   │   ├── Events.vue
│   │   │   ├── Registrations.vue
│   │   │   ├── Results.vue
│   │   │   ├── Announcements.vue
│   │   │   ├── Carousels.vue
│   │   │   └── Feedback.vue
│   │   ├── Login.vue     # 登录页
│   │   ├── Register.vue  # 注册页
│   │   └── NotFound.vue  # 404页面
│   ├── App.vue           # 根组件
│   └── main.js           # 入口文件
├── .env                  # 环境变量
├── .env.development      # 开发环境变量
├── .env.production       # 生产环境变量
├── .gitignore
├── index.html
├── package.json
├── vite.config.js        # Vite配置
└── README.md

```

## 功能特性

### 前台功能
- ✅ 用户注册/登录
- 📋 赛事列表浏览
- 📝 赛事详情查看
- 📢 公告通知查看
- 👤 个人中心管理
- 🎯 赛事报名
- 🏆 成绩查询

### 后台管理
- 📊 数据统计仪表盘
- 👥 用户管理
- 🏅 赛事管理
- 📋 报名审核
- 📈 成绩录入
- 📢 公告发布
- 🖼️ 轮播图管理
- 💬 用户反馈处理

## 开发指南

### 环境要求

- Node.js >= 16.0.0
- npm >= 8.0.0

### 安装依赖

```bash
npm install
```

### 开发模式

```bash
npm run dev
```

访问: http://localhost:5173

### 生产构建

```bash
npm run build
```

### 预览生产构建

```bash
npm run preview
```

## 配置说明

### 环境变量

在 `.env` 文件中配置:

```env
# API基础地址
VITE_API_BASE_URL=http://localhost:8000/api

# 应用标题
VITE_APP_TITLE=体育赛事管理系统

# 上传文件大小限制(MB)
VITE_UPLOAD_SIZE=10
```

### 代理配置

在 `vite.config.js` 中已配置开发服务器代理:

```javascript
server: {
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true
    }
  }
}
```

## API接口说明

所有API接口都封装在 `src/api/` 目录下，统一使用axios实例进行请求。

### 认证方式

使用 JWT Bearer Token 认证:

```javascript
Authorization: Bearer <token>
```

### 请求拦截

- 自动添加Token到请求头
- 统一处理请求错误

### 响应拦截

- 自动处理401/403错误
- 统一错误提示
- Token过期自动跳转登录

## 路由说明

### 前台路由

- `/` - 首页
- `/events` - 赛事列表
- `/events/:id` - 赛事详情
- `/announcements` - 公告列表
- `/profile` - 个人中心 (需登录)
- `/login` - 登录
- `/register` - 注册

### 后台路由 (需管理员权限)

- `/admin` - 管理后台首页
- `/admin/users` - 用户管理
- `/admin/events` - 赛事管理
- `/admin/registrations` - 报名管理
- `/admin/results` - 成绩管理
- `/admin/announcements` - 公告管理
- `/admin/carousels` - 轮播图管理
- `/admin/feedback` - 反馈管理

## 状态管理

使用Vuex进行状态管理，主要模块:

- `user` - 用户信息、登录状态
- `app` - 应用配置、侧边栏状态

## 代码规范

- 使用 Vue 3 Composition API
- 组件使用 `<script setup>` 语法
- 遵循 ESLint 规则
- 统一使用驼峰命名

## 注意事项

1. 确保后端API服务已启动 (http://localhost:8000)
2. 首次登录使用管理员账号访问后台
3. 开发时建议安装 Vue DevTools 浏览器插件
4. 生产环境需要配置正确的API地址

## 待开发功能

当前项目已完成基础架构搭建，包括：

✅ 项目目录结构
✅ 配置文件 (package.json, vite.config.js)
✅ 环境配置
✅ 路由配置
✅ 状态管理
✅ API接口封装
✅ 布局组件
✅ 登录/注册页面
✅ 页面占位组件

下一步需要开发的功能页面：

- 前台首页 (轮播图、赛事推荐等)
- 赛事列表/详情页完整功能
- 个人中心完整功能
- 各个管理后台页面的完整功能

## 许可证

MIT

---

© 2024 体育赛事管理系统
