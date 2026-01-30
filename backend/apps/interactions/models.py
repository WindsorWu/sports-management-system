from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Like(models.Model):
    """点赞模型"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='likes',
        verbose_name='用户'
    )
    # 使用GenericForeignKey支持对多种对象点赞
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name='内容类型'
    )
    object_id = models.PositiveIntegerField(
        verbose_name='对象ID'
    )
    content_object = GenericForeignKey('content_type', 'object_id')
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='点赞时间'
    )
    
    class Meta:
        db_table = 'like'
        verbose_name = '点赞'
        verbose_name_plural = verbose_name
        unique_together = [['user', 'content_type', 'object_id']]
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['user']),
        ]
    
    def __str__(self):
        return f"{self.user.username} 点赞 {self.content_object}"


class Favorite(models.Model):
    """收藏模型"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='用户'
    )
    # 使用GenericForeignKey支持对多种对象收藏
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name='内容类型'
    )
    object_id = models.PositiveIntegerField(
        verbose_name='对象ID'
    )
    content_object = GenericForeignKey('content_type', 'object_id')
    
    remarks = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='备注'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='收藏时间'
    )
    
    class Meta:
        db_table = 'favorite'
        verbose_name = '收藏'
        verbose_name_plural = verbose_name
        unique_together = [['user', 'content_type', 'object_id']]
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['user']),
        ]
    
    def __str__(self):
        return f"{self.user.username} 收藏 {self.content_object}"


class Comment(models.Model):
    """评论模型"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='用户'
    )
    # 使用GenericForeignKey支持对多种对象评论
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name='内容类型'
    )
    object_id = models.PositiveIntegerField(
        verbose_name='对象ID'
    )
    content_object = GenericForeignKey('content_type', 'object_id')
    
    content = models.TextField(
        verbose_name='评论内容'
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='replies',
        verbose_name='父评论',
        help_text='回复某条评论时使用'
    )
    reply_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='received_replies',
        verbose_name='回复给谁'
    )
    is_approved = models.BooleanField(
        default=True,
        verbose_name='是否审核通过'
    )
    like_count = models.IntegerField(
        default=0,
        verbose_name='点赞数'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='评论时间'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='更新时间'
    )
    
    class Meta:
        db_table = 'comment'
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
            models.Index(fields=['user']),
            models.Index(fields=['parent']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username}: {self.content[:50]}"
