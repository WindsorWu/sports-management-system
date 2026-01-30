# 登录401和注册400错误完整修复

## 问题诊断

### 问题1: 登录后401 Unauthorized ❌

**错误流程**:
```
1. 用户登录 → 后端返回 { access: "...", refresh: "..." }
2. 前端Vuex: commit('SET_TOKEN', data.access_token)  ❌ 字段名错误
3. Token未保存 → 获取用户信息时没有token → 401错误
```

**根本原因**:
- 后端返回: `access` 和 `refresh`
- 前端期望: `access_token`

### 问题2: Token存储Key不一致 ❌

**冲突**:
- Vuex store: `localStorage.getItem('token')`
- auth.js: `localStorage.getItem('sports_token')`

**结果**: Token保存和读取使用不同的key

### 问题3: 注册400 Bad Request ❌

**缺少字段**:
- 后端必需: `user_type` (运动员/组织者)
- 前端未提供: 导致400错误

**字段名不匹配**:
- 前端: `full_name`
- 后端期望: `real_name`

---

## 修复方案

### 修复1: 更正Token字段名 ✅

**文件**: `frontend/src/store/modules/user.js`

**修改位置**: 第28-36行

**修改前**:
```javascript
async login({ commit }, loginForm) {
  try {
    const data = await loginApi(loginForm)
    commit('SET_TOKEN', data.access_token)  // ❌ 字段名错误
    setToken(data.access_token)
    return data
  } catch (error) {
    throw error
  }
}
```

**修改后**:
```javascript
async login({ commit }, loginForm) {
  try {
    const data = await loginApi(loginForm)
    // 后端返回的是access和refresh，不是access_token
    commit('SET_TOKEN', data.access)  // ✅ 正确字段名
    setToken(data.access)
    return data
  } catch (error) {
    throw error
  }
}
```

### 修复2: 统一Token存储Key ✅

**文件**: `frontend/src/utils/auth.js`

**修改前**:
```javascript
const TokenKey = 'sports_token'  // ❌ 与Vuex不一致
```

**修改后**:
```javascript
const TokenKey = 'token'  // ✅ 与Vuex保持一致
```

**完整代码**:
```javascript
import Cookies from 'js-cookie'

const TokenKey = 'token'  // 与Vuex store保持一致

export function getToken() {
  return localStorage.getItem(TokenKey)
}

export function setToken(token) {
  localStorage.setItem(TokenKey, token)
  return Cookies.set(TokenKey, token)
}

export function removeToken() {
  localStorage.removeItem(TokenKey)
  return Cookies.remove(TokenKey)
}
```

### 修复3: 修正注册字段映射 ✅

**文件**: `frontend/src/views/Register.vue`

**修改位置**: handleRegister函数

**修改前**:
```javascript
const data = {
  ...registerForm,
  password_confirm: registerForm.confirmPassword
}
delete data.confirmPassword
// ❌ 缺少user_type，字段名未映射
```

**修改后**:
```javascript
// 映射字段名到后端期望的格式
const data = {
  username: registerForm.username,
  email: registerForm.email,
  password: registerForm.password,
  password_confirm: registerForm.confirmPassword,  // 前端字段名转换
  real_name: registerForm.full_name,  // full_name → real_name
  phone: registerForm.phone,
  user_type: 'athlete'  // ✅ 默认注册为运动员
}
```

---

## 后端接口数据结构

### 登录接口

**URL**: `POST /api/auth/login/`

**请求**:
```json
{
  "username": "admin",
  "password": "admin"
}
```

**响应**:
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**字段说明**:
- `access`: 访问令牌（有效期1天）
- `refresh`: 刷新令牌（有效期7天）

### 注册接口

**URL**: `POST /api/users/register/`

**请求**:
```json
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "test123",
  "password_confirm": "test123",
  "real_name": "测试用户",
  "phone": "13800138001",
  "user_type": "athlete"
}
```

**响应**:
```json
{
  "message": "注册成功",
  "user": {
    "id": 2,
    "username": "testuser",
    "email": "test@example.com",
    "real_name": "测试用户",
    "user_type": "athlete"
  }
}
```

---

## 字段映射对照表

### 登录相关

| 前端代码 | 后端返回 | 说明 |
|----------|----------|------|
| `data.access_token` ❌ | `data.access` | 访问令牌 |
| `data.refresh_token` ❌ | `data.refresh` | 刷新令牌 |

### 注册相关

| 前端字段 | 后端字段 | 必填 | 说明 |
|----------|----------|------|------|
| `username` | `username` | ✅ | 用户名 |
| `email` | `email` | ✅ | 邮箱 |
| `password` | `password` | ✅ | 密码 |
| `confirmPassword` | `password_confirm` | ✅ | 确认密码 |
| `full_name` | `real_name` | ✅ | 真实姓名 |
| `phone` | `phone` | ✅ | 手机号 |
| - | `user_type` | ✅ | 用户类型 |

### User_Type 可选值

| 值 | 说明 |
|----|------|
| `athlete` | 运动员（默认） |
| `organizer` | 组织者 |
| `admin` | 管理员（仅后端可设置） |

---

## localStorage数据结构

### 存储的数据

```javascript
// Token
localStorage.getItem('token')
// 值: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

// 用户信息
localStorage.getItem('userInfo')
// 值: JSON字符串
{
  "id": 1,
  "username": "admin",
  "email": "admin@example.com",
  "real_name": "管理员",
  "phone": "13800138000",
  "user_type": "admin",
  "is_superuser": true,
  "is_active": true
}
```

---

## 完整登录流程

```
1. 用户输入用户名密码
   ↓
2. 前端调用: login({ username, password })
   ↓
3. 请求: POST /api/auth/login/
   ↓
4. 后端返回: { access: "...", refresh: "..." }
   ↓
5. 前端保存token:
   - commit('SET_TOKEN', data.access)  ✅ 正确
   - setToken(data.access)
   - localStorage.setItem('token', data.access)
   ↓
6. 前端获取用户信息:
   - GET /api/users/me/
   - Headers: Authorization: Bearer <token>
   ↓
7. 后端返回用户信息
   ↓
8. 前端保存用户信息:
   - commit('SET_USER_INFO', data)
   - localStorage.setItem('userInfo', JSON.stringify(data))
   ↓
9. 跳转到首页
```

---

## 完整注册流程

```
1. 用户填写注册表单
   ↓
2. 前端字段映射:
   - full_name → real_name
   - confirmPassword → password_confirm
   - 添加 user_type: 'athlete'
   ↓
3. 请求: POST /api/users/register/
   ↓
4. 后端验证:
   - 用户名唯一性
   - 邮箱格式
   - 密码匹配
   - 手机号格式
   ↓
5. 创建用户
   ↓
6. 返回: { message: "注册成功", user: {...} }
   ↓
7. 前端提示成功并跳转登录页
```

---

## 测试验证

### 测试登录功能 ✅

**步骤**:
1. 清除localStorage: `localStorage.clear()`
2. 刷新页面
3. 访问: http://localhost:5173/login
4. 输入: admin / admin
5. 点击登录

**预期结果**:
- ✅ 登录成功
- ✅ localStorage中有 `token` 和 `userInfo`
- ✅ 自动跳转到首页
- ✅ 不再出现401错误

**验证localStorage**:
```javascript
// 在Console中执行
console.log('Token:', localStorage.getItem('token'))
console.log('UserInfo:', JSON.parse(localStorage.getItem('userInfo')))
```

### 测试注册功能 ✅

**步骤**:
1. 访问: http://localhost:5173/register
2. 填写表单:
   - 用户名: testuser
   - 邮箱: test@example.com
   - 密码: 123
   - 确认密码: 123
   - 真实姓名: 测试用户
   - 手机号: 13800138001
3. 点击注册

**预期结果**:
- ✅ 注册成功
- ✅ 提示"注册成功，请登录"
- ✅ 跳转到登录页
- ✅ 不再出现400错误

**验证注册成功**:
1. 使用新账号登录
2. ✅ 应该能成功登录

---

## 错误处理优化

### 注册错误信息显示

**改进**:
```javascript
catch (error) {
  const errorMsg = error.response?.data?.detail
    || error.response?.data?.message
    || Object.values(error.response?.data || {}).flat().join(', ')
    || '注册失败'
  ElMessage.error(errorMsg)
}
```

**效果**:
- 显示详细的验证错误信息
- 支持多字段错误提示
- 友好的错误提示

---

## 修复总结

| 问题 | 状态 | 修复内容 |
|------|------|----------|
| 登录401错误 | ✅ 已修复 | Token字段名 access_token → access |
| Token存储不一致 | ✅ 已修复 | 统一使用 'token' 作为key |
| 注册400错误 | ✅ 已修复 | 添加user_type，字段名映射 |
| 字段名映射 | ✅ 已完成 | full_name → real_name |
| 错误提示 | ✅ 已优化 | 显示详细错误信息 |

---

## 操作步骤

### 立即测试

1. **清除localStorage**（重要！）
   ```javascript
   localStorage.clear()
   ```

2. **刷新页面**
   ```
   按 F5
   ```

3. **测试登录**
   - 访问: http://localhost:5173/login
   - 输入: admin / admin
   - ✅ 应该成功登录并跳转首页

4. **测试注册**
   - 访问: http://localhost:5173/register
   - 填写完整信息
   - ✅ 应该注册成功并跳转登录页

---

## 注意事项

### 开发规范

1. **字段名映射**: 前后端字段名不一致时需要映射
2. **必填字段**: 确保所有后端必需字段都提供
3. **错误处理**: 显示详细的错误信息帮助调试
4. **数据验证**: 前端做基础验证，后端做完整验证

### Token管理

1. **存储位置**: localStorage的key必须统一
2. **字段名称**: 使用后端实际返回的字段名
3. **过期处理**: 401时自动清除token并跳转登录页

---

**修复时间**: 2024-01-30
**修复人员**: Claude AI
**版本**: v1.0.6
**状态**: ✅ 已完成

**总结**: 登录401和注册400错误已通过修正Token字段名、统一存储key和完善注册字段映射解决。请清除localStorage后测试。
