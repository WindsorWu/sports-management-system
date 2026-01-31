# 个人中心404错误修复

## 问题描述

**错误信息**:
```
GET http://localhost:5173/api/registrations/me/ 404 (Not Found)
Request failed with status code 404
```

**发生场景**: 访问个人中心时加载"我的报名"数据失败

---

## 问题诊断

### 发现的问题

前端API路径与后端实际路径不匹配：

| 功能 | 前端调用路径 | 后端实际路径 | 状态 |
|------|-------------|-------------|------|
| 我的报名 | `/registrations/me/` ❌ | `/registrations/my_registrations/` | 需修复 |
| 我的成绩 | `/results/me/` ❌ | `/results/my_results/` | 需修复 |
| 我的收藏 | `/interactions/favorites/` ✅ | `/interactions/favorites/` | 正确 |

### 后端接口定义

#### 报名视图 (apps/registrations/views.py)
```python
@action(detail=False, methods=['get'])
def my_registrations(self, request):
    """
    获取当前用户的报名记录
    GET /api/registrations/my_registrations/
    """
```

#### 成绩视图 (apps/results/views.py)
```python
@action(detail=False, methods=['get'])
def my_results(self, request):
    """
    获取当前用户的成绩
    GET /api/results/my_results/
    """
```

#### 收藏视图 (apps/interactions/views.py)
```python
class FavoriteViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        """只返回当前用户的收藏"""
        return self.queryset.filter(user=self.request.user)

# 直接访问 GET /api/interactions/favorites/ 即可
```

---

## 修复方案

### 修复1: 报名接口路径 ✅

**文件**: `frontend/src/api/registration.js`

**修改位置**: 第17-22行

**修改前**:
```javascript
export function getMyRegistrations() {
  return request({
    url: '/registrations/me/',  // ❌ 错误路径
    method: 'get'
  })
}
```

**修改后**:
```javascript
export function getMyRegistrations() {
  return request({
    url: '/registrations/my_registrations/',  // ✅ 正确路径
    method: 'get'
  })
}
```

### 修复2: 成绩接口路径 ✅

**文件**: `frontend/src/api/result.js`

**修改位置**: 第17-22行

**修改前**:
```javascript
export function getMyResults() {
  return request({
    url: '/results/me/',  // ❌ 错误路径
    method: 'get'
  })
}
```

**修改后**:
```javascript
export function getMyResults() {
  return request({
    url: '/results/my_results/',  // ✅ 正确路径
    method: 'get'
  })
}
```

### 修复3: 收藏接口 ✅

**文件**: `frontend/src/api/interaction.js`

**当前配置**:
```javascript
export function getMyFavorites() {
  return request({
    url: '/interactions/favorites/',  // ✅ 已经正确
    method: 'get'
  })
}
```

**说明**: 收藏接口路径已经正确，无需修改。后端通过 `get_queryset()` 自动过滤当前用户的收藏。

---

## API路径规范

### 正确的个人数据接口

| 功能 | 方法 | 路径 | 说明 |
|------|------|------|------|
| 我的报名 | GET | `/api/registrations/my_registrations/` | ✅ |
| 我的成绩 | GET | `/api/results/my_results/` | ✅ |
| 我的收藏 | GET | `/api/interactions/favorites/` | ✅ |
| 当前用户信息 | GET | `/api/users/me/` | ✅ |
| 更新用户信息 | PUT | `/api/users/me/` | ✅ |
| 修改密码 | PUT | `/api/users/me/password/` | ✅ |

### 命名规范说明

**两种命名方式**:

1. **使用 `me`**:
   - 用于用户资源本身
   - 例如: `/users/me/`, `/users/me/password/`

2. **使用 `my_xxx`**:
   - 用于获取用户相关的其他资源列表
   - 例如: `/registrations/my_registrations/`, `/results/my_results/`

**为什么这样设计？**
- `me` 表示"我这个用户"（单数，用户资源）
- `my_xxx` 表示"我的某某列表"（复数，关联资源）

---

## 测试验证

### 测试步骤

1. **清除缓存并登录**
   ```javascript
   localStorage.clear()
   // 然后登录系统
   ```

2. **访问个人中心**
   ```
   http://localhost:5173/profile
   ```

3. **切换Tab标签**
   - 我的报名
   - 我的收藏
   - 我的成绩

4. **预期结果**
   - ✅ 不再出现404错误
   - ✅ 可以正常加载数据
   - ✅ 空数据时显示友好提示
   - ✅ 有数据时正常展示

### 验证接口

#### 测试我的报名
```bash
# 需要先登录获取Token
TOKEN="your_token_here"

curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/registrations/my_registrations/
```

#### 测试我的成绩
```bash
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/results/my_results/
```

#### 测试我的收藏
```bash
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/interactions/favorites/
```

---

## 完整的个人中心数据流

```
用户访问 /profile
  ↓
点击"我的报名"Tab
  ↓
调用 getMyRegistrations()
  ↓
请求 GET /api/registrations/my_registrations/
  ↓
后端ViewSet的my_registrations action处理
  ↓
返回当前用户的报名列表
  ↓
前端展示在表格中
```

---

## 修复总结

| 接口 | 状态 | 修复内容 |
|------|------|----------|
| 我的报名 | ✅ 已修复 | `/me/` → `/my_registrations/` |
| 我的成绩 | ✅ 已修复 | `/me/` → `/my_results/` |
| 我的收藏 | ✅ 正确 | 无需修改 |
| 个人信息 | ✅ 正确 | 保持 `/me/` |

---

## 相关文件

### 修改的文件
1. ✅ `frontend/src/api/registration.js`
2. ✅ `frontend/src/api/result.js`

### 无需修改的文件
- `frontend/src/api/interaction.js` - 收藏接口已正确
- `frontend/src/api/user.js` - 用户信息接口已正确

---

## 开发规范建议

### API命名规范

**推荐做法**:
```javascript
// 获取资源本身
GET /api/users/me/          // 当前用户信息
GET /api/users/me/profile/  // 当前用户的个人资料

// 获取关联资源列表
GET /api/users/my_posts/         // 我的帖子列表
GET /api/registrations/my_registrations/  // 我的报名列表
GET /api/results/my_results/     // 我的成绩列表
```

**避免混淆**:
- 不要在同一个API中混用 `me` 和 `my_xxx`
- 保持命名一致性
- 文档中明确说明路径

### 前后端对接流程

1. **查看后端API文档** - 确认实际路径
2. **编写前端API封装** - 使用正确路径
3. **测试接口调用** - 验证返回数据
4. **页面集成** - 在组件中使用
5. **功能测试** - 端到端测试

---

**修复时间**: 2024-01-30
**修复人员**: Claude AI
**版本**: v1.0.7
**状态**: ✅ 已完成

**总结**: 个人中心的所有API路径已修正，现在可以正常访问和加载数据。请刷新页面后测试个人中心功能。
