from django.db import models
from django.conf import settings


class Announcement(models.Model):
    """公告模型"""
    TYPE_CHOICES = (
        ('system', '系统公告'),
        ('event', '赛事公告'),
        ('news', '新闻资讯'),
        ('notice', '通知'),
    )
    
    PRIORITY_CHOICES = (
        ('low', '低'),
        ('normal', '普通'),
        ('high', '高'),
        ('urgent', '紧急'),
    )
    
    title = models.CharField(
        max_length=200,
        verbose_name='公告标题'
    )
    content = models.TextField(
        verbose_name='公告内容'
    )
    announcement_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default='notice',
        verbose_name='公告类型'
    )
    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default='normal',
        verbose_name='优先级'
    )
    event = models.ForeignKey(
        'events.Event',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='announcements',
        verbose_name='关联赛事',
        help_text='赛事公告需要关联赛事'
    )
    cover_image = models.ImageField(
        upload_to='announcements/%Y/%m/',
        blank=True,
        null=True,
        verbose_name='封面图片'
    )
    attachments = models.FileField(
        upload_to='announcements/files/%Y/%m/',
        blank=True,
        null=True,
        verbose_name='附件'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='announcements',
        verbose_name='发布者'
    )
    is_published = models.BooleanField(
        default=False,
        verbose_name='是否发布'
    )
    is_pinned = models.BooleanField(
        default=False,
        verbose_name='是否置顶'
    )
    view_count = models.IntegerField(
        default=0,
        verbose_name='浏览次数'
    )
    publish_time = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='发布时间'
    )
    expire_time = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='过期时间',
        help_text='过期后不再显示'
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
        ordering = ['-is_pinned', '-publish_time', '-created_at']
        indexes = [
            models.Index(fields=['announcement_type']),
            models.Index(fields=['is_published', '-publish_time']),
            models.Index(fields=['-is_pinned']),
        ]
    
    def __str__(self):
        return self.title
