# 体育赛事管理系统 - 后端

## 概述
提供基于 Django 5.0 与 Django REST Framework 的 REST API 服务，以及通过 Channels 支持的 WebSocket 词云推送，支撑前端页面、管理后台与大屏交互。

## 环境要求
- Python 3.8+
- MySQL 8.0+
- Redis（用于 Channels 缓存/通道，在生产环境建议部署）

## 核心依赖
- `django`、`djangorestframework`、`channels`
- `djangorestframework-simplejwt`（认证）
- `django-filter`（过滤）
- `openpyxl`（Excel 导入/导出）
- `jieba`（词云分词）

## 目录结构概览
- `apps/`: 业务模块（用户、赛事、报名、成绩、互动、轮播、公告、反馈）。
  - `interactions/` 包含评论模型、词云消费者与信号处理。
- `sports_backend/`: 项目配置与路由。
- `utils/`: 权限、分页、导出等公用工具。

## 快速启动
1. 进入 `backend` 目录并安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
2. 生成迁移并同步数据库：
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
3. 创建管理员账号：
   ```bash
   python manage.py createsuperuser
   ```
4. 启动 Django HTTP 服务：
   ```bash
   python manage.py runserver
   ```
5. 启动词云 WebSocket 服务：
   ```bash
   daphne sports_backend.asgi:application --port 8090
   ```
   词云服务通过 `collect_wordcloud_data()` 聚合最近 7 天的 `is_approved=True` 评论，最多保留 400 条、40 个关键词；若数据不足或分词结果为空，前端会继续显示“等待实时词云数据”，但状态仍提示“实时词云更新完成”。

## 词云与消息推送
- `apps.interactions.comment_wordcloud` 会在评论新增、删除或审核状态变化时调度 `broadcast_comment_wordcloud()` 通知 `WORDCLOUD_GROUP`。
- 消息格式为 `{type: "wordcloud_update", payload: [{text, weight}, ...]}`。
- 词云数据的来源与前端状态紧密关联：只要后端返回空数组，前端仍会标记连接成功，但词云画布保持占位提示。

## 智能客服（MaxKB）
- 项目前端通过 MaxKB 实现智能问答与客服，可先通过 Docker 拉起服务：
  ```bash
  docker run -d --name maxkb -p 8080:8080 fittentech/maxkb
  ```
- 启动后在 MaxKB 后台配置知识库或 Token，再在前端页面中嵌入提供的脚本。

## API 参考
详见同级文件 `API_DOC.md`，涵盖认证、用户、赛事、报名、成绩、互动、轮播、公告、反馈与词云的详细接口说明。
