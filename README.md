# 体育赛事管理与报名系统 (Sports Management System)

本项目是一个功能完整的体育赛事管理与报名系统，支持前台展示、在线报名、赛事成绩查询、后台管理以及多种互动功能。采用前后端分离架构开发。

## 项目预览

- **前台系统**：赛事列表、赛事详情、公告动态、在线报名、个人中心、成绩查询、点赞/收藏/评论。
- **后台系统**：用户管理、赛事管理、报名审核、成绩录入与导入、公告管理、轮播图及反馈管理。

## 技术栈

### 后端 (Backend)
- **框架**: Django 5.0.0, Django REST Framework
- **认证**: SimpleJWT (JWT)
- **数据库**: MySQL (通过 PyMySQL 驱动)
- **通信**: Django Channels (WebSocket)
- **工具**: 
  - `openpyxl`: Excel 数据导入导出 (成绩管理)
  - `jieba`: 评论词云处理
  - `Pillow`: 图片处理与上传
  - `django-filter`: API 过滤与搜索

### 前端 (Frontend)
- **框架**: Vue 3 (Composition API)
- **智能客服**: MaxKB (基于 大语言模型 的知识库问答系统)
- **构建工具**: Vite
- **UI 组件库**: Element Plus
- **路由**: Vue Router
- **状态管理**: Vuex
- **图表**: Echarts (数据大屏与词云)
- **网络请求**: Axios
- **日期处理**: Day.js

## 项目结构

```text
sports-management-system/
├── backend/            # Django 后端代码
│   ├── apps/           # 业务应用模块
│   ├── sports_backend/ # 项目配置
│   ├── utils/          # 工具类与辅助函数
│   └── requirements.txt
├── frontend/           # Vue 3 前端代码
│   ├── src/            # 核心源码
│   │   ├── api/        # 接口请求封装
│   │   ├── views/      # 页面组件
│   │   ├── store/      # 状态管理
│   │   └── router/     # 路由配置
│   └── package.json
└── README.md
```

## 快速开始

### Docker 部署 MaxKB (智能客服)
本项目集成了 MaxKB 作为智能客服系统，建议使用 Docker 进行部署：
```bash
docker run -d --name maxkb -p 8080:8080 fittentech/maxkb
```
部署完成后，需在 MaxKB 后台配置知识库与应用，并将嵌入代码集成至前端。

### 后端启动
1. 进入 `backend` 目录。
2. 安装依赖：`pip install -r requirements.txt`。
3. 配置数据库（修改 `sports_backend/settings.py` 中的 DATABASE 配置）。
4. 执行迁移：`python manage.py migrate`。
5. 启动开发服务器：`python manage.py runserver`。

### 前端启动
1. 进入 `frontend` 目录。
2. 安装依赖：`npm install`。
3. 启动开发服务器：`npm run dev`。
4. 编译打包：`npm run build`。

## 功能特性
- **权限管理**: 严谨的角色划分（管理员、裁判、组织者、普通用户）。
- **智能客服**: 集成 MaxKB 智能知识库，提供 7x24 小时赛事咨询服务。
- **赛事流程**: 赛事发布 -> 用户报名 -> 资质审核 -> 成绩录入及排名。
- **互动体验**: 发表评论、点赞收藏、词云分析等。
- **数据处理**: 提供强大的 Excel 成绩导入与导出功能，支持多轮次成绩管理。
