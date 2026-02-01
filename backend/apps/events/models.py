from django.db import models
from django.conf import settings
from apps.results.models import Result
from django.utils import timezone


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

    @property
    def display_status(self):
        """根据比赛时间动态展示已结束状态"""
        if self.status in ('published', 'ongoing') and self.end_time and timezone.now() > self.end_time:
            return 'finished'
        return self.status

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


class EventAssignment(models.Model):
    """赛事裁判任务"""
    ROUND_CHOICES = Result.STATUS_CHOICES

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='assignments',
        verbose_name='赛事'
    )
    referee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='assignments',
        verbose_name='裁判',
        limit_choices_to={'user_type': 'referee'}
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
        ordering = ['-assigned_at']

    def __str__(self):
        return f"{self.event.title} - {self.referee.real_name} - {self.get_round_type_display()}"


class RefereeEventAccess(models.Model):
    """裁判-赛事访问关系"""
    referee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='assigned_events',
        limit_choices_to={'user_type': 'referee'},
        verbose_name='裁判'
    )
    event = models.ForeignKey(
        'Event',
        on_delete=models.CASCADE,
        related_name='referee_accesses',
        verbose_name='赛事'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'referee_event_access'
        verbose_name = '裁判赛事访问'
        verbose_name_plural = verbose_name
        unique_together = ('referee', 'event')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.referee.username} -> {self.event.title}"
