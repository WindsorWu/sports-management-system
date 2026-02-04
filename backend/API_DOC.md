# API 接口文档

本文档概述了体育赛事管理后端的主要 API 接口。

## 认证接口 (`/api/auth/`)
- `POST /api/auth/login/`: 用户登录，获取 Access/Refresh Token。
- `POST /api/auth/refresh/`: 刷新 Token。
- `POST /api/auth/verify/`: 验证 Token。

## 用户管理 (`/api/users/`)
- `POST /api/users/register/`: 用户注册。
- `GET /api/users/me/`: 获取当前登录用户信息。
- `PUT/PATCH /api/users/update_profile/`: 修改个人资料。
- `POST /api/users/change_password/`: 修改密码。
- `GET /api/users/{id}/registrations/`: 查看指定用户的报名记录。
- `GET /api/users/`: 用户列表 (管理员)。

## 赛事管理 (`/api/events/`)
- `GET /api/events/`: 赛事列表 (支持搜索/过滤)。
- `GET /api/events/{id}/`: 赛事详情。
- `POST /api/events/`: 创建赛事 (管理员/组织者)。
- `PUT/PATCH /api/events/{id}/`: 编辑赛事。
- `DELETE /api/events/{id}/`: 删除赛事。
- `GET /api/events/featured/`: 推荐赛事列表。
- `GET /api/events/upcoming/`: 即将开始的赛事。
- `POST /api/events/upload_image/`: 赛事图片上传。

## 报名管理 (`/api/registrations/`)
- `POST /api/registrations/`: 提交报名申请。
- `GET /api/registrations/`: 获取报名列表 (普通用户仅看自己，管理员看全部)。
- `PUT /api/registrations/{id}/approve/`: 审核通过。
- `PUT /api/registrations/{id}/reject/`: 审核拒绝。
- `GET /api/registrations/export/`: 导出报名表为 Excel。

## 成绩管理 (`/api/results/`)
- `GET /api/results/`: 成绩列表，支持按赛事过滤。
- `POST /api/results/`: 手动录入成绩。
- `POST /api/results/batch_import/`: 从 Excel 批量导入成绩。
- `GET /api/results/leaderboard/`: 获取赛事排名榜单。
- `GET /api/results/export/`: 导出成绩表为 Excel。

## 互动功能 (`/api/interactions/`)
- `POST /api/interactions/likes/`: 点赞/取消点赞。
- `POST /api/interactions/favorites/`: 收藏/取消收藏。
- `GET /api/interactions/comments/`: 获取评论列表。
- `POST /api/interactions/comments/`: 发表评论。

## WebSocket 接口
### 评论词云实时更新
- **地址**: `ws://<domain>/ws/comments/wordcloud/`
- **说明**: 
  - 建立连接后，服务端会立即推送当前的词云数据（前40个高频名词/动词）。
  - 当有新的评论通过审核或评论被删除时，服务端会自动向所有连接的客户端推送更新后的词云数据。
- **消息格式**:
  ```json
  {
    "type": "wordcloud_update",
    "payload": [
      {"text": "比赛", "weight": 15},
      {"text": "精彩", "weight": 8},
      ...
    ]
  }
  ```

## 轮播图与公告
- `GET /api/carousels/`: 首页轮播图。
- `GET /api/announcements/`: 公告列表。
- `GET /api/announcements/{id}/`: 公告内容详情。

## 其他说明
- **分页**: 所有列表接口均支持 `page` 和 `page_size` 参数。
- **权限**: 部分接口需要 Header 携带 `Authorization: Bearer <token>`。
- **响应体**: 统一采用 JSON 格式返回。
