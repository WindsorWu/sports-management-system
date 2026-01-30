# 运动赛事管理系统 - 后端模型实现总结

## 📋 项目信息
- **项目路径**: `/e/Python Project/sports-management-system/backend`
- **实施时间**: 2025-01-30
- **Django版本**: 5.1.x
- **Python版本**: 3.13.9

## ✅ 已完成的模块

### 1. 用户模型 (apps.users)
**文件**: `apps/users/models.py`

**核心功能**:
- 扩展 Django AbstractUser
- 用户类型：运动员、组织者、管理员
- 个人信息：姓名、性别、出生日期、身份证
- 联系信息：手机、紧急联系人
- 实名认证标识

**字段**:
- `real_name`: 真实姓名
- `phone`: 手机号 (唯一)
- `user_type`: 用户类型 (athlete/organizer/admin)
- `avatar`: 头像
- `gender`: 性别
- `birth_date`: 出生日期
- `id_card`: 身份证号
- `emergency_contact`: 紧急联系人
- `emergency_phone`: 紧急联系电话
- `organization`: 所属组织
- `bio`: 个人简介
- `is_verified`: 是否实名认证

---

### 2. 赛事模型 (apps.events)
**文件**: `apps/events/models.py`

**核心功能**:
- 赛事全生命周期管理
- 多级赛事分类
- 报名时间控制
- 参赛人数管理

**字段**:
- `title`: 赛事名称
- `description`: 赛事描述
- `cover_image`: 封面图片
- `event_type`: 赛事类型
- `level`: 赛事级别 (国际/国家/省/市/校级)
- `status`: 状态 (草稿/已发布/进行中/已结束/已取消)
- `location`: 比赛地点
- `start_time`: 开始时间
- `end_time`: 结束时间
- `registration_start`: 报名开始时间
- `registration_end`: 报名截止时间
- `max_participants`: 最大参赛人数
- `current_participants`: 当前报名人数
- `registration_fee`: 报名费用
- `rules`: 比赛规则
- `requirements`: 参赛要求
- `prizes`: 奖项设置
- `organizer`: 组织者 (外键到User)
- `contact_person`: 联系人
- `contact_phone`: 联系电话
- `view_count`: 浏览次数
- `is_featured`: 是否推荐

**索引**:
- `(status, -created_at)`
- `event_type`
- `start_time`

---

### 3. 报名模型 (apps.registrations)
**文件**: `apps/registrations/models.py`

**核心功能**:
- 用户报名管理
- 审核流程控制
- 支付状态跟踪
- 报名编号自动生成

**字段**:
- `event`: 赛事 (外键)
- `user`: 用户 (外键)
- `status`: 审核状态 (待审核/已通过/已拒绝/已取消)
- `registration_number`: 报名编号 (唯一)
- `participant_name`: 参赛者姓名
- `participant_phone`: 参赛者电话
- `participant_id_card`: 参赛者身份证
- `participant_gender`: 参赛者性别
- `participant_birth_date`: 参赛者出生日期
- `participant_organization`: 参赛者单位
- `emergency_contact`: 紧急联系人
- `emergency_phone`: 紧急联系电话
- `payment_status`: 支付状态 (未支付/已支付/已退款)
- `payment_amount`: 支付金额
- `payment_time`: 支付时间
- `remarks`: 备注信息
- `review_remarks`: 审核备注
- `reviewed_by`: 审核人 (外键)
- `reviewed_at`: 审核时间

**约束**:
- `unique_together`: `(event, user)` - 同一用户只能报名同一赛事一次

**索引**:
- `status`
- `registration_number`
- `(event, user)`

---

### 4. 成绩模型 (apps.results)
**文件**: `apps/results/models.py`

**核心功能**:
- 比赛成绩记录
- 多轮次支持 (初赛/半决赛/决赛)
- 排名计算
- 奖项管理

**字段**:
- `event`: 赛事 (外键)
- `registration`: 报名记录 (外键)
- `user`: 用户 (外键)
- `round_type`: 轮次 (preliminary/semifinal/final)
- `score`: 成绩 (可以是时间、分数、距离等)
- `rank`: 排名
- `award`: 奖项 (金牌/银牌/铜牌等)
- `score_unit`: 成绩单位 (秒/分/米等)
- `remarks`: 备注
- `certificate_url`: 证书链接
- `is_published`: 是否公开
- `recorded_by`: 录入人 (外键)

**索引**:
- `(event, rank)`
- `user`
- `is_published`

---

### 5. 公告模型 (apps.announcements)
**文件**: `apps/announcements/models.py`

**核心功能**:
- 多类型公告 (系统/赛事/新闻/通知)
- 优先级管理
- 定时发布/过期
- 置顶功能

**字段**:
- `title`: 公告标题
- `content`: 公告内容
- `announcement_type`: 公告类型 (system/event/news/notice)
- `priority`: 优先级 (low/normal/high/urgent)
- `event`: 关联赛事 (外键, 可选)
- `cover_image`: 封面图片
- `attachments`: 附件
- `author`: 发布者 (外键)
- `is_published`: 是否发布
- `is_pinned`: 是否置顶
- `view_count`: 浏览次数
- `publish_time`: 发布时间
- `expire_time`: 过期时间

**排序**: `(-is_pinned, -publish_time, -created_at)`

**索引**:
- `announcement_type`
- `(is_published, -publish_time)`
- `-is_pinned`

---

### 6. 互动模型 (apps.interactions)
**文件**: `apps/interactions/models.py`

**核心功能**:
- 通用点赞系统 (支持多种对象)
- 通用收藏系统
- 评论和回复系统

#### 6.1 点赞模型 (Like)
- 使用 GenericForeignKey 支持对多种对象点赞
- `user`: 点赞用户
- `content_type`: 内容类型
- `object_id`: 对象ID
- `unique_together`: `(user, content_type, object_id)`

#### 6.2 收藏模型 (Favorite)
- 使用 GenericForeignKey 支持对多种对象收藏
- `user`: 收藏用户
- `content_type`: 内容类型
- `object_id`: 对象ID
- `remarks`: 收藏备注
- `unique_together`: `(user, content_type, object_id)`

#### 6.3 评论模型 (Comment)
- 使用 GenericForeignKey 支持对多种对象评论
- `user`: 评论用户
- `content_type`: 内容类型
- `object_id`: 对象ID
- `content`: 评论内容
- `parent`: 父评论 (支持回复)
- `reply_to`: 回复给谁
- `is_approved`: 是否审核通过
- `like_count`: 点赞数

---

### 7. 轮播图模型 (apps.carousel)
**文件**: `apps/carousel/models.py`

**核心功能**:
- 多位置轮播图 (首页/赛事页/公告页)
- 排序控制
- 定时展示
- 点击统计

**字段**:
- `title`: 标题
- `description`: 描述
- `image`: 轮播图片
- `link_url`: 链接地址
- `event`: 关联赛事 (外键, 可选)
- `position`: 展示位置 (home/event/announcement)
- `order`: 排序 (数字越小越靠前)
- `is_active`: 是否启用
- `start_time`: 开始时间
- `end_time`: 结束时间
- `click_count`: 点击次数
- `creator`: 创建者 (外键)

**排序**: `(order, -created_at)`

**索引**:
- `(position, is_active, order)`
- `is_active`

---

### 8. 反馈模型 (apps.feedback)
**文件**: `apps/feedback/models.py`

**核心功能**:
- 多类型反馈 (问题/建议/投诉/表扬/其他)
- 处理流程跟踪
- 图片上传支持
- 匿名反馈支持

**字段**:
- `user`: 用户 (外键)
- `feedback_type`: 反馈类型 (bug/suggestion/complaint/praise/other)
- `title`: 标题
- `content`: 反馈内容
- `images`: 图片列表 (JSONField)
- `contact_info`: 联系方式
- `event`: 关联赛事 (外键, 可选)
- `status`: 处理状态 (pending/processing/resolved/closed)
- `reply`: 回复内容
- `handler`: 处理人 (外键)
- `handled_at`: 处理时间
- `is_anonymous`: 是否匿名

**索引**:
- `(status, -created_at)`
- `feedback_type`
- `user`

---

## 🗄️ 数据库迁移

### 执行的命令:
```bash
# 1. 生成迁移文件
python manage.py makemigrations

# 2. 执行迁移
python manage.py migrate
```

### 迁移结果:
✅ 所有8个应用的迁移文件已成功生成和应用
- users: 1个迁移文件
- events: 2个迁移文件
- registrations: 2个迁移文件
- results: 2个迁移文件
- announcements: 2个迁移文件
- interactions: 2个迁移文件
- carousel: 2个迁移文件
- feedback: 2个迁移文件

---

## 👤 超级管理员账号

### 账号信息:
- **用户名**: `admin`
- **密码**: `admin`
- **邮箱**: `admin@example.com`
- **真实姓名**: 管理员
- **手机号**: `13800138000`
- **用户类型**: `admin`
- **权限**: 超级管理员 (is_superuser=True, is_staff=True)

---

## 📊 数据库表结构

| 应用 | 表名 | 说明 |
|------|------|------|
| users | `user` | 用户表 |
| events | `event` | 赛事表 |
| registrations | `registration` | 报名表 |
| results | `result` | 成绩表 |
| announcements | `announcement` | 公告表 |
| interactions | `like` | 点赞表 |
| interactions | `favorite` | 收藏表 |
| interactions | `comment` | 评论表 |
| carousel | `carousel` | 轮播图表 |
| feedback | `feedback` | 反馈表 |

---

## 🎯 模型特性

### 1. 统一的时间戳
所有模型都包含:
- `created_at`: 创建时间 (auto_now_add=True)
- `updated_at`: 更新时间 (auto_now=True)

### 2. 优化的查询性能
- 所有主要查询字段都添加了索引
- 外键关系使用 `related_name` 方便反向查询
- 使用 `unique_together` 防止重复数据

### 3. 友好的管理界面
- 所有模型都定义了 `verbose_name`
- 字段都包含 `help_text` 说明
- 实现了 `__str__` 方法方便识别

### 4. 灵活的设计
- 使用 GenericForeignKey 实现通用互动功能
- JSONField 存储复杂数据结构
- 状态字段使用 choices 确保数据一致性

---

## 📝 使用建议

### 1. 模型导入
```python
from apps.users.models import User
from apps.events.models import Event
from apps.registrations.models import Registration
from apps.results.models import Result
from apps.announcements.models import Announcement
from apps.interactions.models import Like, Favorite, Comment
from apps.carousel.models import Carousel
from apps.feedback.models import Feedback
```

### 2. 外键关系
```python
# 获取赛事的所有报名记录
event.registrations.all()

# 获取用户的所有报名记录
user.registrations.all()

# 获取赛事的所有成绩
event.results.all()

# 获取用户的所有成绩
user.results.all()
```

### 3. 反向查询
```python
# 获取用户创建的赛事
user.organized_events.all()

# 获取用户创建的公告
user.announcements.all()

# 获取用户的点赞记录
user.likes.all()

# 获取用户的收藏记录
user.favorites.all()
```

---

## 🚀 下一步工作

### 建议的开发顺序:
1. **序列化器 (Serializers)** - 为每个模型创建DRF序列化器
2. **视图 (Views/ViewSets)** - 实现CRUD操作的API视图
3. **权限控制 (Permissions)** - 定义不同用户类型的权限
4. **URL路由 (URLs)** - 配置API路由
5. **Admin后台** - 注册模型到Django Admin
6. **信号处理 (Signals)** - 实现自动化逻辑（如报名成功后增加参赛人数）
7. **测试用例 (Tests)** - 编写单元测试和集成测试
8. **API文档** - 使用drf-yasg生成API文档

---

## ⚠️ 注意事项

1. **外键删除策略**:
   - 大部分外键使用 `CASCADE` (级联删除)
   - 审核人、处理人等使用 `SET_NULL` (设置为空)

2. **文件上传**:
   - 图片和文件会保存到 `media/` 目录
   - 需要在生产环境配置静态文件服务

3. **数据验证**:
   - 手机号、身份证等字段需要在序列化器中添加验证逻辑
   - 报名截止时间、赛事时间等需要业务逻辑验证

4. **性能优化**:
   - 复杂查询使用 `select_related()` 和 `prefetch_related()`
   - 考虑使用缓存优化频繁查询的数据

---

## 📞 技术支持

如有问题，请检查:
1. Django版本是否为 5.1.x
2. 数据库配置是否正确
3. 所有依赖是否已安装

---

**最后更新**: 2025-01-30
**状态**: ✅ 已完成
