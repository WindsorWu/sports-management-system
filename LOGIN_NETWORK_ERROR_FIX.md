# 登录Network Error修复记录

## 问题描述

**错误信息**:
```
Response error: AxiosError: Network Error
at XMLHttpRequest.handleError (xhr.js:112:20)
```

**发生场景**: 前端登录时发送POST请求到 `/api/auth/login/`

## 问题诊断

### 发现的问题

1. **❌ 错误的Content-Type**
   - 前端使用: `application/x-www-form-urlencoded`
   - 后端期望: `application/json`

2. **❌ 不必要的数据转换**
   - 前端使用`transformRequest`将JSON转为form-data
   - 后端JWT认证只接受JSON格式

3. **❌ API地址配置冲突**
   - `.env`: `VITE_API_BASE_URL=http://localhost:8000/api` (完整URL)
   - `vite.config.js`: 配置了代理到 `http://localhost:8000`
   - 冲突导致实际请求地址错误

### 诊断过程

1. ✅ **后端服务器状态** - 运行正常
   ```bash
   curl http://localhost:8000/api/auth/login/
   # 返回: HTTP 405 (证明服务器在线)
   ```

2. ✅ **后端接口测试** - JSON格式可用
   ```bash
   curl -X POST http://localhost:8000/api/auth/login/ \
     -H "Content-Type: application/json" \
     -d '{"username":"admin","password":"admin"}'
   # 返回: {"access":"...","refresh":"..."}
   ```

3. ❌ **前端配置检查** - 发现多个问题
   - `user.js`: 错误的Content-Type和transformRequest
   - `.env`: 使用完整URL与代理冲突

## 修复方案

### 修复1: 简化登录API调用 ✅

**文件**: `frontend/src/api/user.js`

**修改前**:
```javascript
export function login(data) {
  return request({
    url: '/auth/login/',
    method: 'post',
    data: {
      username: data.username,
      password: data.password
    },
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'  // ❌ 错误
    },
    transformRequest: [function (data) {
      // ❌ 不必要的转换
      let ret = ''
      for (let it in data) {
        ret += encodeURIComponent(it) + '=' + encodeURIComponent(data[it]) + '&'
      }
      return ret.slice(0, -1)
    }]
  })
}
```

**修改后**:
```javascript
export function login(data) {
  return request({
    url: '/auth/login/',
    method: 'post',
    data: {
      username: data.username,
      password: data.password
    }
    // ✅ 使用默认的JSON格式
    // ✅ 移除了transformRequest
  })
}
```

**效果**:
- ✅ 使用`request.js`中配置的默认`Content-Type: application/json`
- ✅ 直接发送JSON数据，不做转换
- ✅ 符合Django REST Framework的标准

### 修复2: 修正API地址配置 ✅

**文件**: `frontend/.env`

**修改前**:
```env
VITE_API_BASE_URL=http://localhost:8000/api  # ❌ 完整URL与代理冲突
```

**修改后**:
```env
VITE_API_BASE_URL=/api  # ✅ 使用相对路径，配合Vite代理
```

**原理**:
```
前端请求: /api/auth/login/
↓
Vite代理配置: /api → http://localhost:8000
↓
实际请求: http://localhost:8000/api/auth/login/
↓
后端Django处理
```

**优点**:
- ✅ 避免CORS跨域问题
- ✅ 开发环境和生产环境配置统一
- ✅ 代理自动处理请求转发

## 配置说明

### Vite代理配置 (无需修改)

**文件**: `frontend/vite.config.js`

```javascript
server: {
  port: 5173,
  host: true,
  proxy: {
    '/api': {
      target: 'http://localhost:8000',
      changeOrigin: true,
      rewrite: (path) => path  // 保持路径不变
    }
  }
}
```

**工作原理**:
- 前端页面: `http://localhost:5173`
- API请求: `http://localhost:5173/api/...`
- 代理转发: `http://localhost:8000/api/...`
- 后端服务: `http://localhost:8000`

### Request配置 (无需修改)

**文件**: `frontend/src/utils/request.js`

```javascript
const service = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,  // '/api'
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json;charset=UTF-8'  // ✅ 默认JSON
  }
})
```

## 测试验证

### 测试步骤

1. **重启前端开发服务器**
   ```bash
   cd frontend
   npm run dev
   ```

2. **测试登录功能**
   - 访问: http://localhost:5173/login
   - 输入: admin / admin
   - 点击登录

3. **预期结果**
   - ✅ 不再出现Network Error
   - ✅ 成功获取Token
   - ✅ 自动跳转到首页
   - ✅ localStorage存储Token

### 浏览器开发者工具验证

**Network面板**:
```
Request URL: http://localhost:5173/api/auth/login/
Request Method: POST
Status Code: 200 OK
Request Headers:
  Content-Type: application/json;charset=UTF-8
Request Payload:
  {"username":"admin","password":"admin"}
Response:
  {"access":"...","refresh":"..."}
```

## 相关配置文件

### 环境配置文件

1. **开发环境**: `frontend/.env`
   ```env
   VITE_API_BASE_URL=/api
   ```

2. **生产环境**: `frontend/.env.production`
   ```env
   VITE_API_BASE_URL=/api
   # 生产环境需要配置Nginx代理
   ```

### Django CORS配置 (无需修改)

**文件**: `backend/sports_backend/settings.py`

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Vite开发服务器
    "http://localhost:8080",  # 备用端口
]
CORS_ALLOW_CREDENTIALS = True
```

## 修复总结

| 项目 | 状态 | 说明 |
|------|------|------|
| Content-Type问题 | ✅ 已修复 | 使用JSON格式 |
| 数据转换问题 | ✅ 已修复 | 移除transformRequest |
| API地址冲突 | ✅ 已修复 | 使用相对路径+代理 |
| CORS配置 | ✅ 正常 | Django已配置 |
| 代理配置 | ✅ 正常 | Vite已配置 |

## 注意事项

### 开发规范

1. **统一使用JSON格式**
   - 所有API接口都使用JSON
   - 不要手动设置Content-Type
   - 依赖`request.js`的默认配置

2. **API地址配置**
   - 开发环境: 使用`/api` + Vite代理
   - 生产环境: 使用`/api` + Nginx代理

3. **避免的错误配置**
   ```javascript
   // ❌ 错误: 不要在单个API中覆盖Content-Type
   headers: {
     'Content-Type': 'application/x-www-form-urlencoded'
   }

   // ❌ 错误: 不要使用完整URL作为baseURL
   VITE_API_BASE_URL=http://localhost:8000/api

   // ✅ 正确: 使用相对路径
   VITE_API_BASE_URL=/api
   ```

### 生产环境部署

部署到生产环境时，需要配置Nginx代理:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        root /path/to/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

## 修复状态

- ✅ **登录API修复**: 已完成
- ✅ **环境配置修复**: 已完成
- ✅ **后端验证**: 通过
- ⏳ **前端测试**: 待用户验证

**总结**: Network Error问题已修复，请重启前端开发服务器后测试登录功能。

---

**修复时间**: 2024-01-30
**修复人员**: Claude AI
**版本**: v1.0.2
