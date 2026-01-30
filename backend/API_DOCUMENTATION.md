# 运动赛事管理系统 - API接口文档

## 基础信息

**Base URL**: `http://localhost:8000/api/`

**认证方式**: JWT Bearer Token

## 认证接口

### 1. 用户登录
- **URL**: `/api/auth/login/`
- **Method**: `POST`
- **Body**:
```json
{
  "username": "string",
  "password": "string"
}
```
- **Response**:
```json
{
  "access": "access_token",
  "refresh": "refresh_token"
}
```

### 2. 刷新Token
- **URL**: `/api/auth/refresh/`
- **Method**: `POST`
- **Body**:
```json
{
  "refresh": "refresh_token"
}
```

### 3. 验证Token
- **URL**: `/api/auth/verify/`
- **Method**: `POST`

---

## 用户管理 (/api/users/)

### 用户注册
- **URL**: `/api/users/register/`
- **Method**: `POST`
- **Auth**: 不需要
- **Body**:
```json
{
  "username": "string",
  "email": "string",
  "password": "string",
  "password_confirm": "string",
  "real_name": "string",
  "phone": "string",
  "user_type": "athlete|organizer|admin"
}
```

### 获取当前用户信息
- **URL**: `/api/users/me/`
- **Method**: `GET`
- **Auth**: 必需

### 更新当前用户信息
- **URL**: `/api/users/update_profile/`
- **Method**: `PUT/PATCH`
- **Auth**: 必需

### 修改密码
- **URL**: `/api/users/change_password/`
- **Method**: `POST`
- **Auth**: 必需
- **Body**:
```json
{
  "old_password": "string",
  "new_password": "string",
  "new_password_confirm": "string"
}
```

### 用户列表
- **URL**: `/api/users/`
- **Method**: `GET`
- **Query参数**:
  - `user_type`: 用户类型筛选
  - `search`: 搜索用户名、姓名、手机号等
  - `page`: 页码

### 用户详情
- **URL**: `/api/users/{id}/`
- **Method**: `GET`

### 用户的报名记录
- **URL**: `/api/users/{id}/registrations/`
- **Method**: `GET`

### 用户的成绩记录
- **URL**: `/api/users/{id}/results/`
- **Method**: `GET`

---

## 赛事管理 (/api/events/)

### 赛事列表
- **URL**: `/api/events/`
- **Method**: `GET`
- **Query参数**:
  - `status`: 赛事状态
  - `event_type`: 赛事类型
  - `level`: 赛事级别
  - `search`: 搜索标题、描述、地点

### 创建赛事
- **URL**: `/api/events/`
- **Method**: `POST`
- **Auth**: 必需

### 赛事详情
- **URL**: `/api/events/{id}/`
- **Method**: `GET`

### 更新赛事
- **URL**: `/api/events/{id}/`
- **Method**: `PUT/PATCH`
- **Auth**: 所有者或管理员

### 删除赛事
- **URL**: `/api/events/{id}/`
- **Method**: `DELETE`
- **Auth**: 所有者或管理员

### 点击统计
- **URL**: `/api/events/{id}/click/`
- **Method**: `POST`

### 推荐赛事
- **URL**: `/api/events/featured/`
- **Method**: `GET`

### 即将开始的赛事
- **URL**: `/api/events/upcoming/`
- **Method**: `GET`

### 正在进行的赛事
- **URL**: `/api/events/ongoing/`
- **Method**: `GET`

### 可报名的赛事
- **URL**: `/api/events/can_register/`
- **Method**: `GET`

### 赛事的报名记录
- **URL**: `/api/events/{id}/registrations/`
- **Method**: `GET`

### 赛事的成绩列表
- **URL**: `/api/events/{id}/results/`
- **Method**: `GET`

### 赛事的公告
- **URL**: `/api/events/{id}/announcements/`
- **Method**: `GET`

---

## 报名管理 (/api/registrations/)

### 报名列表
- **URL**: `/api/registrations/`
- **Method**: `GET`
- **Auth**: 必需
- **Query参数**:
  - `status`: 审核状态
  - `event`: 赛事ID
  - `search`: 搜索报名编号、姓名等

### 创建报名
- **URL**: `/api/registrations/`
- **Method**: `POST`
- **Auth**: 必需
- **Body**:
```json
{
  "event": 1,
  "participant_name": "string",
  "participant_phone": "string",
  "participant_id_card": "string",
  "participant_gender": "M|F|O",
  "participant_birth_date": "2000-01-01",
  "participant_organization": "string",
  "emergency_contact": "string",
  "emergency_phone": "string",
  "remarks": "string"
}
```

### 报名详情
- **URL**: `/api/registrations/{id}/`
- **Method**: `GET`
- **Auth**: 必需

### 审核通过
- **URL**: `/api/registrations/{id}/approve/`
- **Method**: `PUT`
- **Auth**: 管理员或组织者
- **Body**:
```json
{
  "review_remarks": "string"
}
```

### 审核拒绝
- **URL**: `/api/registrations/{id}/reject/`
- **Method**: `PUT`
- **Auth**: 管理员或组织者

### 取消报名
- **URL**: `/api/registrations/{id}/cancel/`
- **Method**: `PUT`
- **Auth**: 报名者本人

### 导出报名名单
- **URL**: `/api/registrations/export/`
- **Method**: `GET`
- **Auth**: 管理员或组织者
- **Query参数**:
  - `event`: 赛事ID
  - `status`: 审核状态

### 我的报名记录
- **URL**: `/api/registrations/my_registrations/`
- **Method**: `GET`
- **Auth**: 必需

---

## 成绩管理 (/api/results/)

### 成绩列表
- **URL**: `/api/results/`
- **Method**: `GET`
- **Query参数**:
  - `event`: 赛事ID
  - `user`: 用户ID
  - `round_type`: 轮次
  - `is_published`: 是否公开

### 创建成绩
- **URL**: `/api/results/`
- **Method**: `POST`
- **Auth**: 管理员或组织者
- **Body**:
```json
{
  "event": 1,
  "registration": 1,
  "round_type": "preliminary|semifinal|final",
  "score": "string",
  "rank": 1,
  "award": "string",
  "score_unit": "string",
  "remarks": "string",
  "certificate_url": "string",
  "is_published": true
}
```

### 成绩详情
- **URL**: `/api/results/{id}/`
- **Method**: `GET`

### 更新成绩
- **URL**: `/api/results/{id}/`
- **Method**: `PUT/PATCH`
- **Auth**: 管理员或组织者

### 公开成绩
- **URL**: `/api/results/{id}/publish/`
- **Method**: `PUT`
- **Auth**: 管理员或组织者

### 取消公开成绩
- **URL**: `/api/results/{id}/unpublish/`
- **Method**: `PUT`
- **Auth**: 管理员或组织者

### 导出成绩表
- **URL**: `/api/results/export/`
- **Method**: `GET`
- **Auth**: 管理员或组织者
- **Query参数**:
  - `event`: 赛事ID
  - `round_type`: 轮次

### 排行榜
- **URL**: `/api/results/leaderboard/`
- **Method**: `GET`
- **Query参数**:
  - `event`: 赛事ID（必需）
  - `round_type`: 轮次（默认：final）

### 我的成绩
- **URL**: `/api/results/my_results/`
- **Method**: `GET`
- **Auth**: 必需

---

## 公告管理 (/api/announcements/)

### 公告列表
- **URL**: `/api/announcements/`
- **Method**: `GET`
- **Query参数**:
  - `announcement_type`: 公告类型
  - `priority`: 优先级
  - `is_published`: 是否发布
  - `event`: 关联赛事

### 创建公告
- **URL**: `/api/announcements/`
- **Method**: `POST`
- **Auth**: 必需

### 公告详情
- **URL**: `/api/announcements/{id}/`
- **Method**: `GET`

### 已发布的公告
- **URL**: `/api/announcements/published/`
- **Method**: `GET`

### 置顶公告
- **URL**: `/api/announcements/pinned/`
- **Method**: `GET`

### 发布公告
- **URL**: `/api/announcements/{id}/publish/`
- **Method**: `PUT`
- **Auth**: 所有者或管理员

### 取消发布公告
- **URL**: `/api/announcements/{id}/unpublish/`
- **Method**: `PUT`
- **Auth**: 所有者或管理员

### 置顶
- **URL**: `/api/announcements/{id}/pin/`
- **Method**: `PUT`
- **Auth**: 管理员

### 取消置顶
- **URL**: `/api/announcements/{id}/unpin/`
- **Method**: `PUT`
- **Auth**: 管理员

---

## 互动功能 (/api/interactions/)

### 点赞相关

#### 我的点赞列表
- **URL**: `/api/interactions/likes/`
- **Method**: `GET`
- **Auth**: 必需

#### 点赞
- **URL**: `/api/interactions/likes/`
- **Method**: `POST`
- **Auth**: 必需
- **Body**:
```json
{
  "content_type": 1,
  "object_id": 1
}
```

#### 取消点赞
- **URL**: `/api/interactions/likes/unlike/`
- **Method**: `POST`
- **Auth**: 必需
- **Body**:
```json
{
  "content_type": 1,
  "object_id": 1
}
```

#### 检查是否已点赞
- **URL**: `/api/interactions/likes/check/`
- **Method**: `GET`
- **Auth**: 必需
- **Query参数**: `content_type`, `object_id`

### 收藏相关

#### 我的收藏列表
- **URL**: `/api/interactions/favorites/`
- **Method**: `GET`
- **Auth**: 必需

#### 收藏
- **URL**: `/api/interactions/favorites/`
- **Method**: `POST`
- **Auth**: 必需
- **Body**:
```json
{
  "content_type": 1,
  "object_id": 1,
  "remarks": "string"
}
```

#### 取消收藏
- **URL**: `/api/interactions/favorites/unfavorite/`
- **Method**: `POST`
- **Auth**: 必需

#### 检查是否已收藏
- **URL**: `/api/interactions/favorites/check/`
- **Method**: `GET`
- **Auth**: 必需

### 评论相关

#### 评论列表
- **URL**: `/api/interactions/comments/`
- **Method**: `GET`
- **Query参数**:
  - `content_type`: 内容类型
  - `object_id`: 对象ID
  - `parent`: 父评论ID

#### 创建评论
- **URL**: `/api/interactions/comments/`
- **Method**: `POST`
- **Auth**: 必需
- **Body**:
```json
{
  "content_type": 1,
  "object_id": 1,
  "content": "string",
  "parent": null,
  "reply_to": null
}
```

#### 审核通过
- **URL**: `/api/interactions/comments/{id}/approve/`
- **Method**: `PUT`
- **Auth**: 管理员

#### 审核拒绝
- **URL**: `/api/interactions/comments/{id}/reject/`
- **Method**: `PUT`
- **Auth**: 管理员

#### 点赞评论
- **URL**: `/api/interactions/comments/{id}/like/`
- **Method**: `POST`

---

## 轮播图管理 (/api/carousels/)

### 轮播图列表
- **URL**: `/api/carousels/`
- **Method**: `GET`
- **Query参数**:
  - `position`: 位置
  - `is_active`: 是否启用

### 创建轮播图
- **URL**: `/api/carousels/`
- **Method**: `POST`
- **Auth**: 必需

### 活动的轮播图
- **URL**: `/api/carousels/active/`
- **Method**: `GET`

### 根据位置获取轮播图
- **URL**: `/api/carousels/by_position/`
- **Method**: `GET`
- **Query参数**: `position` (home/event/announcement)

### 点击统计
- **URL**: `/api/carousels/{id}/click/`
- **Method**: `POST`

### 启用轮播图
- **URL**: `/api/carousels/{id}/activate/`
- **Method**: `PUT`
- **Auth**: 所有者或管理员

### 禁用轮播图
- **URL**: `/api/carousels/{id}/deactivate/`
- **Method**: `PUT`
- **Auth**: 所有者或管理员

---

## 反馈管理 (/api/feedbacks/)

### 反馈列表
- **URL**: `/api/feedbacks/`
- **Method**: `GET`
- **Auth**: 必需
- **Query参数**:
  - `feedback_type`: 反馈类型
  - `status`: 处理状态
  - `event`: 关联赛事

### 创建反馈
- **URL**: `/api/feedbacks/`
- **Method**: `POST`
- **Auth**: 必需
- **Body**:
```json
{
  "feedback_type": "bug|suggestion|complaint|praise|other",
  "title": "string",
  "content": "string",
  "images": ["url1", "url2"],
  "contact_info": "string",
  "event": 1,
  "is_anonymous": false
}
```

### 反馈详情
- **URL**: `/api/feedbacks/{id}/`
- **Method**: `GET`
- **Auth**: 必需

### 回复反馈
- **URL**: `/api/feedbacks/{id}/reply/`
- **Method**: `POST`
- **Auth**: 管理员
- **Body**:
```json
{
  "reply": "string",
  "status": "processing|resolved|closed"
}
```

### 更新反馈状态
- **URL**: `/api/feedbacks/{id}/update_status/`
- **Method**: `PUT`
- **Auth**: 管理员
- **Body**:
```json
{
  "status": "processing|resolved|closed"
}
```

### 我的反馈
- **URL**: `/api/feedbacks/my_feedbacks/`
- **Method**: `GET`
- **Auth**: 必需

### 待处理的反馈
- **URL**: `/api/feedbacks/pending/`
- **Method**: `GET`
- **Auth**: 管理员

### 反馈统计
- **URL**: `/api/feedbacks/statistics/`
- **Method**: `GET`
- **Auth**: 管理员

---

## 权限说明

### 用户类型
- `athlete`: 运动员
- `organizer`: 组织者
- `admin`: 管理员

### 权限级别
1. **AllowAny**: 任何人都可以访问
2. **IsAuthenticated**: 需要登录认证
3. **IsOwnerOrAdmin**: 所有者或管理员
4. **IsAdmin**: 仅管理员
5. **IsAdminOrReferee**: 管理员或组织者

---

## 分页说明

所有列表接口都支持分页：
- **Query参数**: `page` (页码), `page_size` (每页数量，默认10)
- **Response格式**:
```json
{
  "count": 100,
  "next": "http://api/endpoint/?page=2",
  "previous": null,
  "results": [...]
}
```

---

## 错误响应格式

```json
{
  "error": "错误信息",
  "detail": "详细信息"
}
```

常见HTTP状态码：
- `200`: 成功
- `201`: 创建成功
- `400`: 请求参数错误
- `401`: 未认证
- `403`: 无权限
- `404`: 资源不存在
- `500`: 服务器错误
