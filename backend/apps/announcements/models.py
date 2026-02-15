from django.db import models
from django.conf import settings


class Announcement(models.Model):
    """
    公告模型
    
    用于发布系统公告、赛事公告、新闻资讯等信息
    
    主要功能:
        - 多类型公告支持（系统、赛事、新闻、通知）
        - 优先级管理（低、普通、高、紧急）
        - 置顶功能
        - 定时发布和过期管理
        - 浏览量统计
        - 支持封面图片和附件
        
    关键字段说明:
        - announcement_type: 公告类型，影响展示位置和样式
        - priority: 优先级，影响显示顺序和醒目程度
        - is_pinned: 是否置顶，置顶公告优先显示
        - is_published: 是否发布，未发布的公告只有创建者可见
        - publish_time: 发布时间，可用于定时发布
        - expire_time: 过期时间，过期后自动隐藏
        
    使用场景:
        - 发布系统维护通知
        - 发布赛事相关公告
        - 发布新闻资讯
        - 发布重要通知
        
    数据表名: announcement
    """
    # 公告类型选项
    TYPE_CHOICES = (
        ('system', '系统公告'),    # 系统级公告，如维护通知、功能更新等
        ('event', '赛事公告'),     # 赛事相关公告，需关联具体赛事
        ('news', '新闻资讯'),      # 新闻类信息，如赛事报道、成果展示等
        ('notice', '通知'),        # 一般性通知
    )
    
    # 优先级选项（从低到高）
    PRIORITY_CHOICES = (
        ('low', '低'),           # 低优先级，一般信息
        ('normal', '普通'),      # 普通优先级，默认级别
        ('high', '高'),          # 高优先级，重要信息
        ('urgent', '紧急'),      # 紧急优先级，需立即关注的信息
    )
    
    # === 基本信息字段 ===
    title = models.CharField(
        max_length=200,
        verbose_name='公告标题',
        help_text='公告的标题，显示在列表中'
    )
    content = models.TextField(
        verbose_name='公告内容',
        help_text='公告的详细内容，支持富文本'
    )
    summary = models.CharField(
        max_length=200,
        blank=True,
        default='',
        verbose_name='摘要',
        help_text='公告摘要，显示在列表中作为简介'
    )
    
    # === 分类和优先级 ===
    announcement_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default='notice',
        verbose_name='公告类型',
        help_text='公告的类型分类'
    )
    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='normal',
        verbose_name='优先级',
        help_text='优先级越高越重要，影响显示顺序'
    )
    
    # === 关联关系 ===
    event = models.ForeignKey(
        'events.Event',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='announcements',
        verbose_name='关联赛事',
        help_text='赛事公告需要关联具体赛事，其他类型可不关联'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='announcements',
        verbose_name='发布者',
        help_text='创建公告的用户'
    )
    
    # === 媒体文件 ===
    cover_image = models.ImageField(
        upload_to='announcements/%Y/%m/',
        blank=True,
        null=True,
        verbose_name='封面图片',
        help_text='公告封面图，显示在列表和详情页'
    )
    attachments = models.FileField(
        upload_to='announcements/files/%Y/%m/',
        blank=True,
        null=True,
        verbose_name='附件',
        help_text='可上传文档、图片等附件'
    )
    
    # === 发布和展示控制 ===
    is_published = models.BooleanField(
        default=False,
        verbose_name='是否发布',
        help_text='未发布的公告只有作者和管理员可见'
    )
    is_pinned = models.BooleanField(
        default=False,
        verbose_name='是否置顶',
        help_text='置顶公告会显示在列表顶部'
    )
    view_count = models.IntegerField(
        default=0,
        verbose_name='浏览次数',
        help_text='公告被查看的次数'
    )
    
    # === 时间管理 ===
    publish_time = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='发布时间',
        help_text='公告的发布时间，可用于定时发布'
    )
    expire_time = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='过期时间',
        help_text='过期后公告将自动隐藏，不再显示'
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
        db_table = 'announcement'
        verbose_name = '公告'
        verbose_name_plural = verbose_name
        # 默认排序：置顶优先，然后按发布时间倒序，最后按创建时间倒序
        ordering = ['-is_pinned', '-publish_time', '-created_at']
        # 数据库索引：优化查询性能
        indexes = [
            models.Index(fields=['announcement_type']),              # 按类型查询
            models.Index(fields=['is_published', '-publish_time']),  # 按发布状态和时间查询
            models.Index(fields=['-is_pinned']),                     # 按置顶状态查询
        ]
    
    def __str__(self):
        """返回公告的字符串表示"""
        return self.title
