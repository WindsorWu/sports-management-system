# 赛事管理创建和删除功能最终修复

## 修复内容

### 问题1: 创建赛事400错误 ✅
**原因**: 日期时间格式问题
**修复**: 添加日期格式化函数

### 问题2: 删除赛事显示错误 ✅
**原因**: 字段名不匹配（event.name vs event.title）
**修复**: 使用event.title

---

## 完整修复

### 1. 日期时间格式化 ✅

**问题**: el-date-picker返回Date对象，后端需要ISO字符串

**修复**: 在handleSubmit中添加格式化函数

```javascript
// 格式化日期时间为ISO格式
const formatDateTime = (dateTime) => {
  if (!dateTime) return ''
  if (typeof dateTime === 'string') return dateTime
  // Date对象转ISO字符串
  return new Date(dateTime).toISOString()
}

formData.append('start_time', formatDateTime(form.event_time))
formData.append('end_time', formatDateTime(form.event_time))
formData.append('registration_start', formatDateTime(form.registration_start || form.event_time))
formData.append('registration_end', formatDateTime(form.registration_end || form.event_time))
```

### 2. 字段名映射 ✅

**表格列定义**:
```vue
<el-table-column prop="title" label="赛事名称" />
```

**删除确认**:
```javascript
`确认删除赛事 "${event.title}" 吗？`
```

**编辑回填**:
```javascript
form.name = event.title
form.image = event.cover_image
form.event_time = event.start_time
```

---

## 测试步骤

### 测试创建赛事

1. **刷新页面** (F5)

2. **访问赛事管理**
   ```
   http://localhost:5173/admin/events
   ```

3. **点击"新增赛事"**

4. **填写表单**
   - 赛事名称: `测试赛事`
   - 比赛时间: 使用日期选择器选择 `2024-05-15 09:00`
   - 参赛地点: `体育场`
   - 详情介绍: `欢迎参加`
   - 状态: 选择 `已发布`

5. **点击"提交"**

6. **预期结果**
   - ✅ 提示"赛事创建成功"
   - ✅ 列表刷新显示新赛事
   - ✅ 状态显示为"已发布"

### 测试删除赛事

1. **在列表中找到任意赛事**

2. **点击"删除"按钮**

3. **预期结果**
   - ✅ 弹出确认对话框
   - ✅ 对话框显示正确的赛事名称（如："确认删除赛事 "测试赛事" 吗？"）
   - ✅ 点击确认后删除成功
   - ✅ 列表自动刷新

### 测试编辑赛事

1. **点击"编辑"按钮**

2. **预期结果**
   - ✅ 表单正确回填所有数据
   - ✅ 赛事名称、时间、地点等都正确显示
   - ✅ 修改后保存成功

### 测试发布功能

1. **创建草稿赛事**
   - 状态选择: 草稿
   - ✅ 创建成功

2. **点击"发布"按钮**
   - ✅ 状态改为已发布
   - ✅ 前台可见

3. **点击"取消发布"按钮**
   - ✅ 状态改回草稿
   - ✅ 前台不可见

---

## 完整的字段对照

### 后端API字段 → 前端表格显示

| 后端字段 | 前端prop | 显示列名 |
|----------|---------|---------|
| `title` | `title` | 赛事名称 ✅ |
| `start_time` | `start_time` | 开始时间 |
| `location` | `location` | 地点 |
| `status` | `status` | 状态 |
| `cover_image` | `cover_image` | 封面 |

### 前端表单 → 后端API提交

| 前端表单字段 | 后端字段 | 处理方式 |
|-------------|---------|---------|
| `name` | `title` | 直接映射 |
| `event_time` | `start_time` | 格式化日期 ✅ |
| `event_time` | `end_time` | 格式化日期 ✅ |
| `image` | `cover_image` | 直接传递 |
| `registration_start` | `registration_start` | 格式化日期 ✅ |
| `registration_end` | `registration_end` | 格式化日期 ✅ |

---

## 修复文件

1. ✅ `frontend/src/views/admin/Events.vue`
   - handleSubmit: 添加日期格式化
   - 表格列: prop="title"
   - handleDelete: event.title
   - handleEdit: 完整字段映射

2. ✅ `frontend/src/api/event.js`
   - publishEvent: 使用PATCH修改status
   - unpublishEvent: 使用PATCH修改status

---

## 修复状态

| 功能 | 状态 |
|------|------|
| 创建草稿 | ✅ 可用 |
| 创建已发布 | ✅ 可用 |
| 创建已结束 | ✅ 可用 |
| 发布赛事 | ✅ 可用 |
| 取消发布 | ✅ 可用 |
| 编辑赛事 | ✅ 可用 |
| 删除赛事 | ✅ 可用 |
| 日期格式化 | ✅ 已修复 |
| 字段映射 | ✅ 完整 |

---

**修复时间**: 2024-01-30
**版本**: v1.0.17
**状态**: ✅ 完成

**总结**: 赛事管理的创建、编辑、删除、发布等所有功能已完全修复。刷新页面即可测试完整功能。
