# 赛事发布功能修复

## 问题描述

**错误**: POST /api/events/1/publish/ 404 (Not Found)
**场景**: 创建草稿后尝试发布时失败

---

## 问题原因

### 后端没有publish/unpublish接口

检查后端 `apps/events/views.py`，发现：
- ❌ 没有 `@action publish` 方法
- ❌ 没有 `@action unpublish` 方法
- ✅ 只能通过修改 `status` 字段来改变状态

---

## 修复方案

### 方案：通过PATCH修改status实现发布 ✅

**文件**: `frontend/src/api/event.js`

**修改前**（调用不存在的接口）:
```javascript
export function publishEvent(id) {
  return request({
    url: `/events/${id}/publish/`,  // ❌ 后端没有这个接口
    method: 'post'
  })
}

export function unpublishEvent(id) {
  return request({
    url: `/events/${id}/unpublish/`,  // ❌ 后端没有这个接口
    method: 'post'
  })
}
```

**修改后**（修改status字段）:
```javascript
export function publishEvent(id) {
  return request({
    url: `/events/${id}/`,
    method: 'patch',  // ✅ 使用PATCH
    data: { status: 'published' }  // ✅ 修改status
  })
}

export function unpublishEvent(id) {
  return request({
    url: `/events/${id}/`,
    method: 'patch',  // ✅ 使用PATCH
    data: { status: 'draft' }  // ✅ 改回草稿
  })
}
```

---

## 赛事状态流转

### 状态选项

| 状态值 | 中文名称 | 说明 |
|--------|---------|------|
| `draft` | 草稿 | 未发布，仅管理员可见 |
| `published` | 已发布 | 公开，可报名 |
| `ongoing` | 进行中 | 比赛正在进行 |
| `finished` | 已结束 | 比赛已结束 |
| `cancelled` | 已取消 | 赛事取消 |

### 状态流转逻辑

```
draft（草稿）
  ↓ 发布
published（已发布）
  ↓ 开始比赛
ongoing（进行中）
  ↓ 结束比赛
finished（已结束）

或者从任何状态 → cancelled（取消）
```

### 实现方式

**发布赛事**:
```javascript
// PATCH /api/events/1/
{ status: 'published' }
```

**取消发布**:
```javascript
// PATCH /api/events/1/
{ status: 'draft' }
```

**开始比赛**:
```javascript
// PATCH /api/events/1/
{ status: 'ongoing' }
```

**结束比赛**:
```javascript
// PATCH /api/events/1/
{ status: 'finished' }
```

---

## 前端使用说明

### 创建已发布的赛事

**方式1: 创建时直接选择状态**
1. 点击"新增赛事"
2. 填写表单
3. 状态选择: `已发布`
4. 点击提交
5. ✅ 直接创建为已发布状态

**方式2: 先创建草稿再发布**
1. 创建草稿状态的赛事
2. 在列表中找到该赛事
3. 点击"发布"按钮
4. ✅ 状态改为已发布

### 状态切换

在赛事列表中：
- 草稿状态 → 点击"发布"按钮 → 已发布
- 已发布状态 → 点击"取消发布"按钮 → 草稿

---

## 测试验证

### 测试1: 直接创建已发布的赛事

1. 刷新页面 (F5)
2. 访问: http://localhost:5173/admin/events
3. 点击"新增赛事"
4. 填写表单:
   - 赛事名称: `2024春季运动会`
   - 比赛时间: 2024-05-01 09:00
   - 参赛地点: `学校操场`
   - 详情介绍: `欢迎参加`
   - **状态: 选择`已发布`** ← 关键
5. 点击"提交"
6. **预期结果**:
   - ✅ 创建成功
   - ✅ 状态显示为"已发布"
   - ✅ 前台可以看到该赛事

### 测试2: 草稿发布

1. 创建一个草稿状态的赛事
2. 在列表中点击"发布"按钮
3. **预期结果**:
   - ✅ 提示"发布成功"
   - ✅ 状态变为"已发布"
   - ✅ 列表自动刷新

### 测试3: 取消发布

1. 找到已发布的赛事
2. 点击"取消发布"按钮
3. **预期结果**:
   - ✅ 提示"取消发布成功"
   - ✅ 状态变为"草稿"
   - ✅ 前台不再显示该赛事

---

## 修复总结

| 项目 | 状态 | 修复内容 |
|------|------|----------|
| publishEvent | ✅ 已修复 | 使用PATCH修改status |
| unpublishEvent | ✅ 已修复 | 使用PATCH修改status |
| 直接创建已发布 | ✅ 可用 | 表单选择状态 |
| 草稿转发布 | ✅ 可用 | 点击按钮切换 |
| 404错误 | ✅ 已解决 | 不再调用不存在的接口 |

---

## 后续建议

### 如果需要更复杂的发布逻辑

可以在后端添加publish action来实现：

```python
# backend/apps/events/views.py

@action(detail=True, methods=['post'])
def publish(self, request, pk=None):
    """发布赛事"""
    event = self.get_object()

    # 检查是否可以发布（如：信息是否完整）
    if not event.cover_image:
        return Response({'error': '请先上传封面图片'}, status=400)

    event.status = 'published'
    event.save()

    return Response({'message': '发布成功'})
```

但目前通过PATCH修改status已经足够使用。

---

**修复时间**: 2024-01-30
**版本**: v1.0.15
**状态**: ✅ 已完成

**总结**: 赛事发布功能已通过修改status字段的方式实现。刷新页面即可测试创建已发布状态的赛事或发布草稿赛事。
