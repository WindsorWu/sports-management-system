# 体育赛事管理系统 - 后端

基于 Django 5.0 和 Django REST Framework 开发的后端 API 接口系统。

## 环境要求
- Python 3.8+
- MySQL 8.0+
- Redis (用于 Channels/Cache)

## 核心依赖
- `Django`: Web 框架核心
- `djangorestframework`: API 开发插件
- `djangorestframework-simplejwt`: JWT 认证管理
- `django-cors-headers`: 处理跨域请求
- `django-filter`: 提供强大的 API 过滤功能
- `openpyxl`: 处理成绩与报名的 Excel 导出导入
- `jieba`: 分词处理，用于互动评论的词云分析
- `channels`: 构建异步通信支持

## 目录结构
- `apps/`: 存放所有业务应用
  - `users/`: 用户、角色与权限管理
  - `events/`: 赛事信息发布、分类与图片管理
  - `registrations/`: 报名流程、状态审核
  - `results/`: 成绩登记、排名计算与批量导入
  - `announcements/`: 公告动态
  - `interactions/`: 点赞、收藏、评论、词云
  - `carousel/`: 首页轮播图管理
  - `feedback/`: 意见反馈
- `sports_backend/`: 全局配置、主路由、ASGI/WSGI 配置
- `utils/`: 共通工具
  - `permissions.py`: 自定义权限类 (IsAdmin, IsReferee 等)
  - `export.py`: 导出功能封装
  - `pagination.py`: 分页格式定义

## 部署说明
1. **安装依赖**:
   ```bash
   pip install -r requirements.txt
   ```
2. **初始化数据库**:
   创建 MySQL 数据库，并在 `sports_backend/settings.py` 或 `.env` 中配置连接。
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
3. **创建超级管理员**:
   ```bash
   python manage.py createsuperuser
   ```
4. **运行项目**:
   ```bash
   python manage.py runserver
   ```
5. **启动词云服务 (WebSocket)**:
   ```bash
   daphne sports_backend.asgi:application --port 8090
   ```

## 开发者文档
- API 接口列表详见 `API_DOC.md`。
- 系统权限逻辑基于 `user_type` 字段判定：`admin` (管理员), `referee` (裁判), `organizer` (组织者), `user` (普通用户)。
