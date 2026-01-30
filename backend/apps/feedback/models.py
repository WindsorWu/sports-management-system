from django.db import models
from django.conf import settings


class Feedback(models.Model):
    """反馈模型"""
    TYPE_CHOICES = (
        ('bug', '问题反馈'),
        ('suggestion', '功能建议'),
        ('complaint', '投诉'),
        ('praise', '表扬'),
        ('other', '其他'),
    )
    
    STATUS_CHOICES = (
        ('pending', '待处理'),
        ('processing', '处理中'),
        ('resolved', '已解决'),
        ('closed', '已关闭'),
    )
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='feedbacks',
        verbose_name='用户'
    )
    feedback_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default='suggestion',
        verbose_name='反馈类型'
    )
    title = models.CharField(
        max_length=200,
        verbose_name='标题'
    )
    content = models.TextField(
        verbose_name='反馈内容'
    )
    images = models.JSONField(
        blank=True,
        null=True,
        verbose_name='图片列表',
        help_text='存储多张图片的URL列表'
    )
    contact_info = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='联系方式',
        help_text='用户的联系方式'
    )
    event = models.ForeignKey(
        'events.Event',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='feedbacks',
        verbose_name='关联赛事',
        help_text='如果是关于某个赛事的反馈'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='处理状态'
    )
    reply = models.TextField(
        blank=True,
        null=True,
        verbose_name='回复内容'
    )
    handler = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='handled_feedbacks',
        verbose_name='处理人'
    )
    handled_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='处理时间'
    )
    is_anonymous = models.BooleanField(
        default=False,
        verbose_name='是否匿名',
        help_text='匿名反馈不显示用户信息'
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
        db_table = 'feedback'
        verbose_name = '反馈'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['feedback_type']),
            models.Index(fields=['user']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"
