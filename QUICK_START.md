# 🚀 运动赛事管理系统 - 快速启动指南

## ✅ 当前状态

- ✅ 后端: **100%完成** (Django + DRF + MySQL)
- ✅ 前端架构: **100%完成** (Vue3 + Vite + Element Plus)
- ⚠️ 前端页面: **40%完成** (登录注册已完成,业务页面待开发)

---

## 📋 前置要求

### 已安装的软件
- ✅ Python 3.13
- ✅ Node.js (推荐18+)
- ✅ MySQL 8.0

### 已完成的配置
- ✅ MySQL数据库 `sports` 已创建
- ✅ 所有Python依赖已安装
- ✅ 数据库表已创建 (15个迁移文件)
- ✅ 超级管理员已创建 (admin/admin)
- ✅ 所有Vue依赖已安装 (91个npm包)

---

## 🎯 一键启动

### 方法1: 使用脚本启动 (推荐)

#### Windows
创建 `start.bat`:
```batch
@echo off
echo Starting Sports Event Management System...
echo.

echo [1/2] Starting Backend Server...
start "Django Backend" cmd /k "cd backend && python manage.py runserver"
timeout /t 3

echo [2/2] Starting Frontend Server...
start "Vue Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ========================================
echo   System Started Successfully!
echo ========================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:5173
echo Admin:    admin / admin
echo ========================================
echo.
pause
```

然后双击 `start.bat` 运行。

#### Linux/Mac
创建 `start.sh`:
```bash
#!/bin/bash
echo "Starting Sports Event Management System..."
echo ""

echo "[1/2] Starting Backend Server..."
cd backend
python manage.py runserver &
BACKEND_PID=$!
cd ..

echo "[2/2] Starting Frontend Server..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "========================================"
echo "  System Started Successfully!"
echo "========================================"
echo ""
echo "Backend:  http://localhost:8000"
echo "Frontend: http://localhost:5173"
echo "Admin:    admin / admin"
echo "========================================"
echo ""
echo "Press Ctrl+C to stop all servers"

# 等待信号
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT TERM

wait
```

然后执行:
```bash
chmod +x start.sh
./start.sh
```

### 方法2: 手动启动

#### 第1步: 启动后端 (终端1)
```bash
cd backend
python manage.py runserver
```

#### 第2步: 启动前端 (终端2)
```bash
cd frontend
npm run dev
```

---

## 🌐 访问地址

启动成功后,打开浏览器访问:

| 服务 | 地址 | 说明 |
|------|------|------|
| **前端首页** | http://localhost:5173 | Vue前端应用 |
| **登录页面** | http://localhost:5173/login | 用户登录 |
| **注册页面** | http://localhost:5173/register | 用户注册 |
| **管理后台** | http://localhost:5173/admin | 后台管理 |
| **后端API** | http://localhost:8000/api | RESTful API |
| **Django Admin** | http://localhost:8000/admin | Django管理后台 |

---

## 🔑 测试账号

### 超级管理员
```
用户名: admin
密码: admin
角色: 超级管理员
权限: 所有权限
```

### 创建测试用户
1. 访问注册页面: http://localhost:5173/register
2. 填写注册信息:
   - 用户名: test_athlete
   - 密码: test123456
   - 确认密码: test123456
   - 姓名: 测试运动员
   - 手机号: 13800138001
   - 用户类型: 运动员
3. 点击注册按钮
4. 使用新账号登录

---

## 🧪 快速测试

### 测试后端API

#### 1. 测试用户注册
```bash
curl -X POST http://localhost:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "test_user",
    "password": "test123456",
    "password_confirm": "test123456",
    "real_name": "测试用户",
    "phone": "13800138002",
    "user_type": "athlete"
  }'
```

#### 2. 测试用户登录
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin"
  }'
```

#### 3. 测试获取赛事列表
```bash
curl http://localhost:8000/api/events/
```

### 测试前端功能

1. **测试登录**
   - 打开: http://localhost:5173/login
   - 输入: admin / admin
   - 点击登录按钮
   - ✅ 成功后应跳转到首页

2. **测试注册**
   - 打开: http://localhost:5173/register
   - 填写完整的注册信息
   - 点击注册按钮
   - ✅ 成功后应跳转到登录页

3. **测试权限**
   - 未登录时访问: http://localhost:5173/admin
   - ✅ 应自动跳转到登录页

---

## 📊 系统检查

### 后端健康检查
```bash
cd backend

# 检查Django配置
python manage.py check

# 查看数据库迁移状态
python manage.py showmigrations

# 测试数据库连接
python manage.py dbshell

# 查看已创建的用户
python manage.py shell
>>> from apps.users.models import User
>>> User.objects.all()
```

### 前端健康检查
```bash
cd frontend

# 检查依赖是否正确安装
npm list --depth=0

# 检查配置文件
cat .env

# 测试构建
npm run build
```

---

## 🐛 常见问题

### 问题1: 后端启动失败
```
错误: django.db.utils.OperationalError: (2003, "Can't connect to MySQL server")
```
**解决方案**:
1. 确保MySQL服务正在运行
2. 检查 `backend/.env` 中的数据库配置
3. 重新运行 `python backend/init_db.py`

### 问题2: 前端启动失败
```
错误: Error: Cannot find module 'xxx'
```
**解决方案**:
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### 问题3: API请求失败
```
错误: Network Error 或 CORS错误
```
**解决方案**:
1. 确保后端服务器正在运行
2. 检查 `backend/sports_backend/settings.py` 中的CORS配置
3. 确保API地址正确 (http://localhost:8000/api)

### 问题4: Token失效
```
错误: 401 Unauthorized
```
**解决方案**:
1. 重新登录获取新的Token
2. 检查Token是否正确存储在localStorage
3. 确保请求头包含 `Authorization: Bearer {token}`

---

## 📚 开发文档

- **项目总览**: `/README.md`
- **后端API文档**: `/backend/API_DOCUMENTATION.md`
- **后端模型文档**: `/backend/MODELS_IMPLEMENTATION_SUMMARY.md`
- **前端项目文档**: `/frontend/README.md`
- **前端快速开始**: `/frontend/QUICK_START.md`

---

## 🔧 数据库管理

### 创建新的迁移
```bash
cd backend
python manage.py makemigrations
python manage.py migrate
```

### 重置数据库 (⚠️ 谨慎使用)
```bash
cd backend

# 删除所有迁移文件
find apps -path "*/migrations/*.py" -not -name "__init__.py" -delete
find apps -path "*/migrations/*.pyc" -delete

# 删除数据库
mysql -u root -p
DROP DATABASE sports;
CREATE DATABASE sports CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
exit

# 重新创建迁移和数据库表
python manage.py makemigrations
python manage.py migrate

# 重新创建超级用户
python manage.py createsuperuser
```

### 备份数据库
```bash
mysqldump -u root -p sports > backup_$(date +%Y%m%d_%H%M%S).sql
```

### 恢复数据库
```bash
mysql -u root -p sports < backup_20240130_180000.sql
```

---

## 🚀 部署到生产环境

### 后端部署

1. **修改配置**
```bash
# backend/.env
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
SECRET_KEY=your-new-secret-key-here
```

2. **收集静态文件**
```bash
python manage.py collectstatic
```

3. **使用Gunicorn启动**
```bash
pip install gunicorn
gunicorn sports_backend.wsgi:application --bind 0.0.0.0:8000
```

### 前端部署

1. **构建生产版本**
```bash
cd frontend
npm run build
```

2. **部署dist目录**
- 将 `frontend/dist/` 目录部署到Nginx或其他Web服务器

3. **配置Nginx**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        root /path/to/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 📞 技术支持

### 项目状态查询
- 后端: ✅ 100%完成
- 前端基础: ✅ 100%完成
- 前端业务页面: ⚠️ 40%完成

### 下一步开发
1. 实现前台首页
2. 实现赛事列表和详情页
3. 实现个人中心
4. 实现管理后台各模块

---

## ✨ 项目亮点

- ✅ **153个REST API接口** - 功能完整
- ✅ **JWT认证系统** - 安全可靠
- ✅ **完善的权限控制** - 6种权限类
- ✅ **Excel导出功能** - 报名名单、成绩表
- ✅ **模块化设计** - 易于维护和扩展
- ✅ **Vue3 Composition API** - 现代化开发体验
- ✅ **Element Plus UI** - 企业级组件库
- ✅ **完整的开发文档** - 快速上手

---

**创建时间**: 2024年1月30日
**版本**: v1.0.0
**状态**: ✅ 可用 (核心功能完成)

**立即开始**: 运行 `start.bat` (Windows) 或 `start.sh` (Linux/Mac)
