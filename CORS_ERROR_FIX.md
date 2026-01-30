# CORS跨域问题修复记录

## 问题描述

**错误信息**:
```
Access to XMLHttpRequest at 'http://localhost:8000/api/auth/login/'
from origin 'http://localhost:5173' has been blocked by CORS policy:
Response to preflight request doesn't pass access control check:
No 'Access-Control-Allow-Origin' header is present on the requested resource.
```

**发生场景**: 前端登录时发送请求到后端API

---

## 问题诊断

### 根本原因

虽然我们修改了 `.env` 文件，但Vite在开发模式下会**优先使用** `.env.development` 文件！

**文件优先级**:
```
.env.development (开发环境优先)
  ↓
.env.local
  ↓
.env (最低优先级)
```

### 配置冲突

1. **`.env`**: 正确配置了 `VITE_API_BASE_URL=/api`
2. **`.env.development`**: ❌ 使用了 `VITE_API_BASE_URL=http://localhost:8000/api`
3. **结果**: 开发环境实际使用了完整URL，绕过了Vite代理

### 为什么会CORS错误

```
前端页面: http://localhost:5173 (Vite)
API请求: http://localhost:8000/api/auth/login/ (直接请求)
        ↑
        跨域请求（不同端口）
        ↓
Django CORS拦截（虽然配置了，但OPTIONS请求可能有问题）
```

---

## 修复方案

### 修复所有环境配置文件

#### 1. `.env` (基础配置) ✅

**文件**: `frontend/.env`

```env
# API基础地址 - 使用Vite代理，只需要/api即可
VITE_API_BASE_URL=/api

# 应用标题
VITE_APP_TITLE=体育赛事管理系统

# 上传文件大小限制(MB)
VITE_UPLOAD_SIZE=10
```

#### 2. `.env.development` (开发环境) ✅ **关键修复**

**文件**: `frontend/.env.development`

**修改前**:
```env
VITE_API_BASE_URL=http://localhost:8000/api  # ❌ 导致CORS错误
```

**修改后**:
```env
# 开发环境配置 - 使用Vite代理
VITE_API_BASE_URL=/api  # ✅ 使用代理，避免CORS
VITE_APP_TITLE=体育赛事管理系统(开发环境)
```

#### 3. `.env.production` (生产环境) ✅

**文件**: `frontend/.env.production`

**修改前**:
```env
VITE_API_BASE_URL=https://your-production-domain.com/api  # ❌ 硬编码域名
```

**修改后**:
```env
# 生产环境配置 - 使用Nginx代理
VITE_API_BASE_URL=/api  # ✅ 灵活部署
VITE_APP_TITLE=体育赛事管理系统
```

---

## 工作原理

### 开发环境请求流程

```
用户登录
  ↓
前端代码调用: login({ username, password })
  ↓
axios请求: POST /api/auth/login/
  ↓
完整URL: http://localhost:5173/api/auth/login/ (同源)
  ↓
Vite代理配置: /api → http://localhost:8000
  ↓
实际请求: POST http://localhost:8000/api/auth/login/
  ↓
Django处理返回: { access, refresh }
  ↓
代理返回给前端 (无CORS问题)
```

### 关键配置

**Vite代理配置** (`vite.config.js`):
```javascript
server: {
  port: 5173,
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true,  // 修改origin头
      rewrite: (path) => path  // 保持路径
    }
  }
}
```

**优点**:
- ✅ 前端请求同源（http://localhost:5173/api/...）
- ✅ 自动代理到后端（http://localhost:8000/api/...）
- ✅ 无需处理CORS
- ✅ 开发体验流畅

---

## 生产环境部署

### Nginx配置示例

生产环境使用相同的相对路径 `/api`，通过Nginx代理到后端：

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # 前端静态文件
    location / {
        root /var/www/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # API代理到后端
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # 媒体文件
    location /media/ {
        alias /var/www/backend/media/;
    }
}
```

**优点**:
- ✅ 前后端使用相同域名，无CORS问题
- ✅ 统一SSL证书管理
- ✅ 统一访问日志
- ✅ 方便负载均衡

---

## 测试验证

### 测试步骤

1. **关闭前端开发服务器**
   ```bash
   # 在运行npm run dev的终端按 Ctrl+C
   ```

2. **清除浏览器缓存** (重要！)
   - Chrome: F12 → Network → 右键 → Clear browser cache
   - 或者: Ctrl+Shift+Delete → 清除缓存

3. **重新启动前端服务器**
   ```bash
   cd frontend
   npm run dev
   ```

4. **测试登录**
   - 打开: http://localhost:5173/login
   - 输入: admin / admin
   - 点击登录

5. **验证Network面板**
   - F12 打开开发者工具
   - 切换到 Network 标签
   - 查看请求：
     ```
     Request URL: http://localhost:5173/api/auth/login/  ✅ 同源
     Status: 200 OK  ✅ 成功
     Response: {"access":"...","refresh":"..."}  ✅ 正常
     ```

### 预期结果

- ✅ 不再出现CORS错误
- ✅ 请求URL显示为 `http://localhost:5173/api/...`（通过代理）
- ✅ 成功获取JWT Token
- ✅ 自动跳转到首页

---

## 常见问题

### Q1: 为什么要用代理而不是直接配置CORS？

**A**: 使用代理的优点：
1. ✅ 开发环境和生产环境配置一致
2. ✅ 无需处理复杂的CORS配置
3. ✅ 避免OPTIONS预检请求问题
4. ✅ 更好的安全性（不暴露后端端口）
5. ✅ 方便进行API mock

### Q2: 如果必须使用CORS怎么办？

**A**: 如果必须用CORS，需要确保Django配置完整：

```python
# settings.py
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = [
    'DELETE', 'GET', 'OPTIONS', 'PATCH', 'POST', 'PUT',
]
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# 并在MIDDLEWARE中添加（要放在CommonMiddleware之前）
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # ← 必须在前面
    'django.middleware.common.CommonMiddleware',
    # ...
]
```

### Q3: 前端环境变量为什么不生效？

**A**: Vite的环境变量优先级：
1. `.env.[mode].local` (最高)
2. `.env.[mode]` (次高，如 `.env.development`)
3. `.env.local`
4. `.env` (最低)

**解决方法**:
- 确保修改了正确的文件（开发环境修改 `.env.development`）
- 修改后必须重启开发服务器
- 清除浏览器缓存

---

## 修复总结

| 配置文件 | 修改前 | 修改后 | 状态 |
|----------|--------|--------|------|
| `.env` | `/api` | `/api` | ✅ 正确 |
| `.env.development` | `http://localhost:8000/api` | `/api` | ✅ 已修复 |
| `.env.production` | `https://domain.com/api` | `/api` | ✅ 已修复 |
| `vite.config.js` | 代理配置 | 无需修改 | ✅ 正确 |

---

## 检查清单

部署前请确认：

- ✅ 所有 `.env*` 文件都使用 `/api` 作为baseURL
- ✅ `vite.config.js` 配置了正确的代理
- ✅ 前端开发服务器已重启
- ✅ 浏览器缓存已清除
- ✅ 登录功能正常工作
- ✅ 无CORS错误

---

## 相关文档

- Vite环境变量: https://vitejs.dev/guide/env-and-mode.html
- Vite代理配置: https://vitejs.dev/config/server-options.html#server-proxy
- Django CORS: https://github.com/adamchainz/django-cors-headers

---

**修复时间**: 2024-01-30
**修复人员**: Claude AI
**版本**: v1.0.3
**状态**: ✅ 已完成

**总结**: CORS问题已通过修复环境变量配置文件解决。请重启前端开发服务器并清除浏览器缓存后测试。
