# API 接口文档

本文档概述体育赛事管理系统后端服务的主要 REST API 和 WebSocket 接口，所有路径默认以 `/api/` 开头（除 WebSocket）。

## 通用约定
- 所有列表接口均支持分页（`page` 与 `page_size`），返回的 `results` 内包含当前页数据。分页大小可通过 `PAGE_SIZE` 预设或请求参数调整。
- 认证：所有需登录权限的接口必须在 `Authorization: Bearer <access_token>` Header 中传递 JWT。
- 过滤与排序：部分端点支持 `search`、`ordering` 和 `filterset_fields`，具体见各模块说明。

## 认证接口 `/api/auth/`
- `POST /api/auth/login/`：用户名/密码登录，返回 `access` 与 `refresh`。
- `POST /api/auth/refresh/`：刷新 Access Token。
- `POST /api/auth/verify/`：验证 Token 是否有效。

## 用户管理 `/api/users/`
- `GET /api/users/`：管理员获取用户列表。
- `POST /api/users/`：注册同一用户（仅限无 Token 的请求）。
- `GET /api/users/{id}/`：查看指定用户。
- `PUT/PATCH /api/users/{id}/`：管理员或本人更新用户信息。
- `POST /api/users/{id}/change_password/`：管理员重置或本人修改密码。

## 赛事管理 `/api/events/`
- `GET /api/events/`：赛事列表，支持 `search`、`ordering` 与分类过滤。
- `GET /api/events/{id}/`：赛事详情。
- `POST /api/events/`：管理员/组织者创建赛事。
- `PUT/PATCH /api/events/{id}/`：维护赛事信息。
- `DELETE /api/events/{id}/`：删除赛事。
- `GET /api/events/featured/`：推荐赛事。
- `GET /api/events/upcoming/`：即将开始赛事。
- `POST /api/events/upload_image/`：上传封面。

## 报名管理 `/api/registrations/`
- `POST /api/registrations/`：提交报名申请，自动与当前用户绑定。
- `GET /api/registrations/`：筛选用户报名记录，管理员可查看全部。
- `PUT /api/registrations/{id}/approve/`：审核通过。
- `PUT /api/registrations/{id}/reject/`：审核拒绝。
- `GET /api/registrations/export/`：导出 Excel 报名单。

## 成绩管理 `/api/results/`
- `GET /api/results/`：查询成绩，支持赛事过滤。
- `POST /api/results/`：录入单条成绩。
- `POST /api/results/batch_import/`：批量从 Excel 上传。
- `GET /api/results/leaderboard/`：获取排名榜。
- `GET /api/results/export/`：导出成绩表。

## 公告与轮播 `/api/announcements/` `/api/carousels/`
- `GET /api/announcements/`、`GET /api/carousels/`：列表。
- `GET /api/announcements/{id}/`：公告详情。
- 管理员可通过对应管理后台录入、编辑、删除。

## 反馈 `/api/feedbacks/`
- `GET /api/feedbacks/`：管理员查看所有反馈。
- `POST /api/feedbacks/`：访客/用户提交问题。
- `PUT/PATCH /api/feedbacks/{id}/process/`：标记状态或回复（需权限）。

## 互动 `/api/interactions/`
### 点赞 `/api/interactions/likes/`
- `POST /api/interactions/likes/`：点赞，传 `content_type` + `object_id`。
- `GET /api/interactions/likes/check/`：查询当前用户是否点赞。
- `POST /api/interactions/likes/unlike/`：取消点赞。

### 收藏 `/api/interactions/favorites/`
- `POST /api/interactions/favorites/`：收藏。
- `GET /api/interactions/favorites/check/`：确认收藏状态。
- `POST /api/interactions/favorites/unfavorite/`：取消收藏。

### 评论 `/api/interactions/comments/`
- `GET /api/interactions/comments/`：获取评论列表，默认仅显示 `is_approved=True` 的记录。
- `POST /api/interactions/comments/`：发布评论，需要登录。
- `PUT /api/interactions/comments/{id}/`：更新（仅作者或管理员）。
- `DELETE /api/interactions/comments/{id}/`：删除。
- `PUT /api/interactions/comments/{id}/approve/`：审核通过。
- `PUT /api/interactions/comments/{id}/reject/`：审核拒绝。
- `POST /api/interactions/comments/{id}/like/`：点赞指定评论。

## 实时评论词云（WebSocket）
- **地址**：`ws://<域名或 IP>:8090/ws/comments/wordcloud/`，前端根据 `VITE_API_BASE_URL`+端口动态解析。
- **启动**：使用 `daphne sports_backend.asgi:application --port 8090` 启动异步服务，确保 `channels` 渠道层可用。
- **数据来源**：仅整理最近 7 天内 `is_approved=True` 的评论，最多从 400 条中挑选；分词只保留中文名词、形容词+名词、动词+名词，最多输出 40 个关键词。
- **消息格式**：
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
- **前端状态**：若 payload 为空或仅包含无效词汇，前端会继续显示“等待实时词云数据”，而状态仍提示“实时词云更新完成”，因为 WebSocket 连接已收到空更新。

## 通信与额外说明
- **消息推送**：`broadcast_comment_wordcloud()` 在评论创建、删除（及审核）后触发，会将分词结果广播至 `admin_comment_wordcloud` 频道。
- **分页与过滤**：所有 `/api/` 列表接口支持 `page`、`page_size`；部分支持 `search`、`ordering`、`filterset_fields`。
- **权限**：默认使用 Django REST Framework 的 `IsAuthenticatedOrReadOnly`，但各视图会适配 `IsOwnerOrAdmin`、`IsAdmin` 等。
- **静态/媒体**：开发模式下 `STATIC_URL` 与 `MEDIA_URL` 提供文件访问，详见 `sports_backend/settings.py`。
