from django.db import models
from django.conf import settings
from apps.results.models import Result
from django.utils import timezone


class Event(models.Model):
    """
    赛事模型
    
    存储体育赛事的完整信息，包括赛事基本信息、时间安排、
    报名设置、联系方式等
    
    主要功能:
        - 赛事发布和管理
        - 报名时间和人数控制
        - 赛事状态管理（草稿、已发布、进行中、已结束、已取消）
        - 赛事级别分类（国际级到校级）
        
    关键字段说明:
        - status: 赛事状态，影响赛事的可见性和报名
        - max_participants: 最大参赛人数，0表示不限制
        - current_participants: 当前报名人数，由报名系统更新
        - is_featured: 是否推荐到首页展示
        
    数据表名: event
    """
    # 赛事状态选项
    STATUS_CHOICES = (
        ('draft', '草稿'),           # 草稿状态，仅创建者可见
        ('published', '已发布'),     # 已发布，用户可见可报名
        ('ongoing', '进行中'),       # 比赛进行中
        ('finished', '已结束'),      # 比赛已结束
        ('cancelled', '已取消'),     # 赛事已取消
    )
    
    # 赛事级别选项（从高到低）
    LEVEL_CHOICES = (
        ('international', '国际级'),  # 国际性赛事
        ('national', '国家级'),       # 全国性赛事
        ('provincial', '省级'),       # 省级赛事
        ('city', '市级'),            # 市级赛事
        ('school', '校级'),          # 校级赛事
    )
    
    # === 基本信息字段 ===
    title = models.CharField(
        max_length=200,
        verbose_name='赛事名称'
    )
    description = models.TextField(
        verbose_name='赛事描述',
        help_text='详细的赛事介绍'
    )
    cover_image = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name='封面图片',
        help_text='图片路径，如：/images/events/xxx.jpg'
    )
    event_type = models.CharField(
        max_length=50,
        verbose_name='赛事类型',
        help_text='如：田径、游泳、篮球等'
    )
    level = models.CharField(
        max_length=20,
        choices=LEVEL_CHOICES,
        default='school',
        verbose_name='赛事级别'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft',            # 新创建的赛事默认为草稿
        verbose_name='赛事状态'
    )
    location = models.CharField(
        max_length=200,
        verbose_name='比赛地点'
    )
    
    # === 时间安排字段 ===
    start_time = models.DateTimeField(
        verbose_name='开始时间'
    )
    end_time = models.DateTimeField(
        verbose_name='结束时间'
    )
    registration_start = models.DateTimeField(
        verbose_name='报名开始时间'
    )
    registration_end = models.DateTimeField(
        verbose_name='报名截止时间'
    )
    
    # === 报名设置字段 ===
    max_participants = models.IntegerField(
        default=0,
        verbose_name='最大参赛人数',
        help_text='0表示不限制'
    )
    current_participants = models.IntegerField(
        default=0,
        verbose_name='当前报名人数'
    )
    registration_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='报名费用',
        help_text='单位：元'
    )
    
    # === 详细信息字段 ===
    rules = models.TextField(
        blank=True,
        null=True,
        verbose_name='比赛规则'
    )
    requirements = models.TextField(
        blank=True,
        null=True,
        verbose_name='参赛要求'
    )
    prizes = models.TextField(
        blank=True,
        null=True,
        verbose_name='奖项设置'
    )
    
    # === 组织者和联系信息 ===
    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='organized_events',  # 反向查询：user.organized_events
        verbose_name='组织者'
    )
    contact_person = models.CharField(
        max_length=50,
        verbose_name='联系人'
    )
    contact_phone = models.CharField(
        max_length=11,
        verbose_name='联系电话'
    )
    contact_email = models.EmailField(
        blank=True,
        null=True,
        verbose_name='联系邮箱'
    )
    
    # === 统计和展示字段 ===
    view_count = models.IntegerField(
        default=0,
        verbose_name='浏览次数'
    )
    is_featured = models.BooleanField(
        default=False,
        verbose_name='是否推荐',
        help_text='推荐到首页展示'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='更新时间'
    )

    @property
    def display_status(self):
        """
        动态展示状态属性
        
        根据赛事的结束时间自动判断实际状态
        如果赛事标记为published或ongoing，但结束时间已过，
        则自动返回finished状态
        
        返回:
            str: 赛事的实际展示状态
        """
        if self.status in ('published', 'ongoing') and self.end_time and timezone.now() > self.end_time:
            return 'finished'
        return self.status

    class Meta:
        db_table = 'event'
        verbose_name = '赛事'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']  # 默认按创建时间倒序
        # 数据库索引，优化常用查询
        indexes = [
            models.Index(fields=['status', '-created_at']),  # 状态和时间组合查询
            models.Index(fields=['event_type']),              # 按类型查询
            models.Index(fields=['start_time']),              # 按开始时间排序
        ]
    
    def __str__(self):
        """字符串表示：返回赛事标题"""
        return self.title


class EventAssignment(models.Model):
    """
    赛事裁判任务模型
    
    用于将裁判员分配到特定赛事的特定轮次
    管理裁判的工作任务和责任范围
    
    主要功能:
        - 将裁判分配到赛事
        - 指定裁判负责的比赛轮次（预赛、半决赛、决赛等）
        - 记录任务分配人和时间
        - 添加任务备注
    
    使用场景:
        - 赛事组织者为不同轮次分配裁判
        - 裁判查看自己的工作任务列表
        - 管理员统计裁判工作量
        
    数据表名: event_assignment
    """
    # 轮次选项，从Result模型复用
    ROUND_CHOICES = Result.STATUS_CHOICES

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='assignments',  # 反向查询：event.assignments
        verbose_name='赛事'
    )
    referee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='assignments',  # 反向查询：user.assignments
        verbose_name='裁判',
        limit_choices_to={'user_type': 'referee'}  # 限制只能选择裁判类型的用户
    )
    round_type = models.CharField(
        max_length=20,
        choices=ROUND_CHOICES,
        verbose_name='轮次'
    )
    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='assigned_results',
        null=True,
        blank=True,
        verbose_name='分配人'
    )
    assigned_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='分配时间'
    )
    remarks = models.TextField(
        blank=True,
        null=True,
        verbose_name='备注'
    )

    class Meta:
        db_table = 'event_assignment'
        verbose_name = '赛事任务'
        verbose_name_plural = verbose_name
        ordering = ['-assigned_at']  # 按分配时间倒序

    def __str__(self):
        """
        字符串表示
        格式: "赛事标题 - 裁判姓名 - 轮次"
        """
        return f"{self.event.title} - {self.referee.real_name} - {self.get_round_type_display()}"


class RefereeEventAccess(models.Model):
    """
    裁判-赛事访问关系模型
    
    控制裁判员对赛事数据的访问权限
    决定裁判可以查看和管理哪些赛事的报名和成绩信息
    
    主要功能:
        - 为裁判分配赛事访问权限
        - 控制裁判的数据访问范围
        - 实现基于赛事的权限隔离
    
    使用场景:
        - 管理员为裁判分配可管理的赛事
        - 裁判登录后只能看到有权限的赛事
        - 实现多个裁判分工管理不同赛事
    
    唯一约束:
        - (referee, event) 组合唯一，防止重复分配
        
    数据表名: referee_event_access
    """
    referee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='assigned_events',  # 反向查询：referee.assigned_events
        limit_choices_to={'user_type': 'referee'},  # 限制只能选择裁判
        verbose_name='裁判'
    )
    event = models.ForeignKey(
        'Event',
        on_delete=models.CASCADE,
        related_name='referee_accesses',  # 反向查询：event.referee_accesses
        verbose_name='赛事'
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name='创建时间'
    )

    class Meta:
        db_table = 'referee_event_access'
        verbose_name = '裁判赛事访问'
        verbose_name_plural = verbose_name
        unique_together = ('referee', 'event')  # 同一裁判不能重复分配同一赛事
        ordering = ['-created_at']

    def __str__(self):
        """
        字符串表示
        格式: "裁判用户名 -> 赛事标题"
        """
        return f"{self.referee.username} -> {self.event.title}"
