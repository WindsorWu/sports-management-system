from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Like(models.Model):
    """
    点赞模型
    
    通用的点赞功能，支持对多种对象点赞（赛事、公告等）
    
    主要功能:
        - 通用点赞: 使用GenericForeignKey支持对任意模型点赞
        - 唯一性约束: 同一用户对同一对象只能点赞一次
        - 点赞统计: 记录点赞时间
        
    关键字段说明:
        - content_type: 被点赞对象的模型类型
        - object_id: 被点赞对象的ID
        - content_object: GenericForeignKey，指向被点赞的对象
        
    使用方式:
        # 为赛事点赞
        Like.objects.create(
            user=user,
            content_type=ContentType.objects.get_for_model(Event),
            object_id=event_id
        )
        
    使用场景:
        - 为赛事点赞
        - 为公告点赞
        - 为评论点赞
        
    数据表名: like
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='likes',
        verbose_name='用户',
        help_text='点赞的用户'
    )
    # 使用GenericForeignKey支持对多种对象点赞
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name='内容类型',
        help_text='被点赞对象的模型类型'
    )
    object_id = models.PositiveIntegerField(
        verbose_name='对象ID',
        help_text='被点赞对象的ID'
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
        # 唯一性约束：同一用户对同一对象只能点赞一次
        unique_together = [['user', 'content_type', 'object_id']]
        ordering = ['-created_at']
        # 数据库索引：优化查询性能
        indexes = [
            models.Index(fields=['content_type', 'object_id']),  # 查询某对象的所有点赞
            models.Index(fields=['user']),                        # 查询用户的所有点赞
        ]
    
    def __str__(self):
        """返回点赞的字符串表示"""
        return f"{self.user.username} 点赞 {self.content_object}"


class Favorite(models.Model):
    """
    收藏模型
    
    通用的收藏功能，支持对多种对象收藏（赛事、公告等）
    
    主要功能:
        - 通用收藏: 使用GenericForeignKey支持对任意模型收藏
        - 唯一性约束: 同一用户对同一对象只能收藏一次
        - 备注功能: 可以为收藏添加个人备注
        - 收藏统计: 记录收藏时间
        
    关键字段说明:
        - content_type: 被收藏对象的模型类型
        - object_id: 被收藏对象的ID
        - content_object: GenericForeignKey，指向被收藏的对象
        - remarks: 用户可以添加收藏备注
        
    使用场景:
        - 收藏感兴趣的赛事
        - 收藏重要公告
        - 建立个人收藏列表
        
    数据表名: favorite
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='用户',
        help_text='收藏的用户'
    )
    # 使用GenericForeignKey支持对多种对象收藏
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name='内容类型',
        help_text='被收藏对象的模型类型'
    )
    object_id = models.PositiveIntegerField(
        verbose_name='对象ID',
        help_text='被收藏对象的ID'
    )
    content_object = GenericForeignKey('content_type', 'object_id')
    
    remarks = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='备注',
        help_text='用户可以添加收藏备注'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='收藏时间'
    )
    
    class Meta:
        db_table = 'favorite'
        verbose_name = '收藏'
        verbose_name_plural = verbose_name
        # 唯一性约束：同一用户对同一对象只能收藏一次
        unique_together = [['user', 'content_type', 'object_id']]
        ordering = ['-created_at']
        # 数据库索引：优化查询性能
        indexes = [
            models.Index(fields=['content_type', 'object_id']),  # 查询某对象的所有收藏
            models.Index(fields=['user']),                        # 查询用户的所有收藏
        ]
    
    def __str__(self):
        """返回收藏的字符串表示"""
        return f"{self.user.username} 收藏 {self.content_object}"


class Comment(models.Model):
    """
    评论模型
    
    通用的评论功能，支持对多种对象评论，支持评论回复
    
    主要功能:
        - 通用评论: 使用GenericForeignKey支持对任意模型评论
        - 评论回复: 支持评论的多级回复
        - 评论审核: 支持评论审核机制
        - 点赞统计: 评论可以被点赞
        
    关键字段说明:
        - content_type: 被评论对象的模型类型
        - object_id: 被评论对象的ID
        - content_object: GenericForeignKey，指向被评论的对象
        - parent: 父评论，用于评论回复
        - reply_to: 回复给谁，用于@功能
        - is_approved: 是否审核通过
        - like_count: 评论的点赞数
        
    使用场景:
        - 为赛事评论
        - 为公告评论
        - 回复其他用户的评论
        
    数据表名: comment
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='用户',
        help_text='发表评论的用户'
    )
    # 使用GenericForeignKey支持对多种对象评论
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name='内容类型',
        help_text='被评论对象的模型类型'
    )
    object_id = models.PositiveIntegerField(
        verbose_name='对象ID',
        help_text='被评论对象的ID'
    )
    content_object = GenericForeignKey('content_type', 'object_id')
    
    content = models.TextField(
        verbose_name='评论内容',
        help_text='评论的文本内容'
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='replies',
        verbose_name='父评论',
        help_text='回复某条评论时使用，指向被回复的评论'
    )
    reply_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='received_replies',
        verbose_name='回复给谁',
        help_text='@某个用户时使用'
    )
    is_approved = models.BooleanField(
        default=True,
        verbose_name='是否审核通过',
        help_text='未审核通过的评论不会公开显示'
    )
    like_count = models.IntegerField(
        default=0,
        verbose_name='点赞数',
        help_text='评论获得的点赞数量'
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
        # 数据库索引：优化查询性能
        indexes = [
            models.Index(fields=['content_type', 'object_id']),  # 查询某对象的所有评论
            models.Index(fields=['user']),                        # 查询用户的所有评论
            models.Index(fields=['parent']),                      # 查询某评论的所有回复
            models.Index(fields=['-created_at']),                 # 按时间排序
        ]
    
    def __str__(self):
        """返回评论的字符串表示"""
        return f"{self.user.username}: {self.content[:50]}"
