# 🚀 快速参考指南

## 超级管理员账号
```
用户名: admin
密码: admin
邮箱: admin@example.com
手机: 13800138000
```

## 数据库操作

### 创建迁移
```bash
python manage.py makemigrations
```

### 执行迁移
```bash
python manage.py migrate
```

### 查看迁移状态
```bash
python manage.py showmigrations
```

### 回滚迁移
```bash
python manage.py migrate <app_name> <migration_number>
```

## 常用命令

### 启动开发服务器
```bash
python manage.py runserver
python manage.py runserver 0.0.0.0:8000
```

### 创建超级用户
```bash
python manage.py createsuperuser
```

### 进入Django Shell
```bash
python manage.py shell
```

### 收集静态文件
```bash
python manage.py collectstatic
```

## 模型快速查询

### 用户相关
```python
from apps.users.models import User

# 获取所有用户
users = User.objects.all()

# 获取特定用户
user = User.objects.get(username='admin')

# 创建用户
user = User.objects.create_user(
    username='test',
    email='test@example.com',
    password='password123',
    real_name='测试用户',
    phone='13900139000'
)
```

### 赛事相关
```python
from apps.events.models import Event

# 获取所有已发布的赛事
events = Event.objects.filter(status='published')

# 获取进行中的赛事
ongoing_events = Event.objects.filter(status='ongoing')

# 创建赛事
event = Event.objects.create(
    title='2025年春季田径运动会',
    description='...',
    event_type='田径',
    organizer=user,
    # ... 其他字段
)
```

### 报名相关
```python
from apps.registrations.models import Registration

# 获取某赛事的所有报名
registrations = Registration.objects.filter(event=event)

# 获取已通过的报名
approved = Registration.objects.filter(status='approved')

# 创建报名
registration = Registration.objects.create(
    event=event,
    user=user,
    participant_name=user.real_name,
    # ... 其他字段
)
```

### 成绩相关
```python
from apps.results.models import Result

# 获取某赛事的所有成绩（按排名）
results = Result.objects.filter(event=event).order_by('rank')

# 获取某用户的所有成绩
user_results = Result.objects.filter(user=user)

# 创建成绩
result = Result.objects.create(
    event=event,
    registration=registration,
    user=user,
    score='12.50',
    rank=1,
    award='金牌'
)
```

### 公告相关
```python
from apps.announcements.models import Announcement

# 获取所有已发布的公告
announcements = Announcement.objects.filter(is_published=True)

# 获取置顶公告
pinned = Announcement.objects.filter(is_pinned=True)

# 创建公告
announcement = Announcement.objects.create(
    title='重要通知',
    content='...',
    announcement_type='notice',
    author=user
)
```

### 互动相关
```python
from apps.interactions.models import Like, Favorite, Comment
from django.contrib.contenttypes.models import ContentType

# 点赞
event_type = ContentType.objects.get_for_model(Event)
like = Like.objects.create(
    user=user,
    content_type=event_type,
    object_id=event.id
)

# 收藏
favorite = Favorite.objects.create(
    user=user,
    content_type=event_type,
    object_id=event.id,
    remarks='很棒的赛事'
)

# 评论
comment = Comment.objects.create(
    user=user,
    content_type=event_type,
    object_id=event.id,
    content='期待这次比赛！'
)

# 回复评论
reply = Comment.objects.create(
    user=another_user,
    content_type=event_type,
    object_id=event.id,
    content='我也是！',
    parent=comment,
    reply_to=user
)
```

## 数据库表映射

| 模型 | 数据库表名 |
|------|-----------|
| User | user |
| Event | event |
| Registration | registration |
| Result | result |
| Announcement | announcement |
| Like | like |
| Favorite | favorite |
| Comment | comment |
| Carousel | carousel |
| Feedback | feedback |

## 状态选项

### 用户类型 (user_type)
- `athlete`: 运动员
- `organizer`: 组织者
- `admin`: 管理员

### 赛事状态 (status)
- `draft`: 草稿
- `published`: 已发布
- `ongoing`: 进行中
- `finished`: 已结束
- `cancelled`: 已取消

### 报名状态 (status)
- `pending`: 待审核
- `approved`: 已通过
- `rejected`: 已拒绝
- `cancelled`: 已取消

### 支付状态 (payment_status)
- `unpaid`: 未支付
- `paid`: 已支付
- `refunded`: 已退款

### 公告类型 (announcement_type)
- `system`: 系统公告
- `event`: 赛事公告
- `news`: 新闻资讯
- `notice`: 通知

### 反馈类型 (feedback_type)
- `bug`: 问题反馈
- `suggestion`: 功能建议
- `complaint`: 投诉
- `praise`: 表扬
- `other`: 其他

## 文件上传路径

- 用户头像: `media/avatars/YYYY/MM/`
- 赛事封面: `media/events/YYYY/MM/`
- 公告封面: `media/announcements/YYYY/MM/`
- 公告附件: `media/announcements/files/YYYY/MM/`
- 轮播图: `media/carousel/YYYY/MM/`

## 环境配置

### .env 文件示例
```env
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_NAME=sports_db
DATABASE_USER=root
DATABASE_PASSWORD=your-password
DATABASE_HOST=localhost
DATABASE_PORT=3306
```

## 常见问题

### Q: 如何重置数据库？
```bash
# 删除所有迁移文件（保留__init__.py）
# 删除数据库
# 重新运行
python manage.py makemigrations
python manage.py migrate
```

### Q: 如何导出数据？
```bash
python manage.py dumpdata > backup.json
python manage.py dumpdata users.User > users.json
```

### Q: 如何导入数据？
```bash
python manage.py loaddata backup.json
```

### Q: 如何清空某个表？
```python
from apps.users.models import User
User.objects.all().delete()
```

## 开发建议

1. **使用虚拟环境**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **代码格式化**
   ```bash
   black .
   flake8 .
   ```

4. **运行测试**
   ```bash
   python manage.py test
   ```

5. **查看SQL语句**
   ```python
   from django.db import connection
   print(connection.queries)
   ```

---

更多详细信息请参考 `MODELS_IMPLEMENTATION_SUMMARY.md`
