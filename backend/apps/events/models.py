from django.db import models
from django.conf import settings


class Event(models.Model):
    """赛事模型"""
    STATUS_CHOICES = (
        ('draft', '草稿'),
        ('published', '已发布'),
        ('ongoing', '进行中'),
        ('finished', '已结束'),
        ('cancelled', '已取消'),
    )
    
    LEVEL_CHOICES = (
        ('international', '国际级'),
        ('national', '国家级'),
        ('provincial', '省级'),
        ('city', '市级'),
        ('school', '校级'),
    )
    
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
        default='draft',
        verbose_name='赛事状态'
    )
    location = models.CharField(
        max_length=200,
        verbose_name='比赛地点'
    )
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
    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='organized_events',
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
    
    class Meta:
        db_table = 'event'
        verbose_name = '赛事'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['event_type']),
            models.Index(fields=['start_time']),
        ]
    
    def __str__(self):
        return self.title
