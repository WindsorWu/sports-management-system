from django.db import models
from django.conf import settings


class Feedback(models.Model):
    """
    反馈模型
    
    用于用户向系统提交反馈意见和问题报告
    
    主要功能:
        - 多类型反馈: 支持问题反馈、功能建议、投诉、表扬等
        - 反馈处理: 管理员可以回复和处理反馈
        - 状态跟踪: 跟踪反馈的处理状态
        - 匿名支持: 用户可以选择匿名提交
        - 图片上传: 支持上传问题截图
        
    关键字段说明:
        - feedback_type: 反馈类型，影响处理优先级
        - status: 处理状态，从待处理到已解决
        - is_anonymous: 是否匿名，匿名反馈不显示用户信息
        - reply: 管理员的回复内容
        - handler: 处理反馈的管理员
        - images: 反馈相关的图片
        
    使用场景:
        - 用户报告bug
        - 用户提出功能建议
        - 用户投诉或表扬
        - 系统改进参考
        
    数据表名: feedback
    """
    # 反馈类型选项
    TYPE_CHOICES = (
        ('bug', '问题反馈'),       # 系统bug或问题
        ('suggestion', '功能建议'), # 功能改进建议
        ('complaint', '投诉'),     # 投诉相关
        ('praise', '表扬'),        # 表扬反馈
        ('other', '其他'),         # 其他类型反馈
    )
    
    # 处理状态选项
    STATUS_CHOICES = (
        ('pending', '待处理'),     # 新提交，等待处理
        ('processing', '处理中'),  # 正在处理
        ('resolved', '已解决'),    # 已处理完成
        ('closed', '已关闭'),      # 已关闭，不再处理
    )
    
    # === 基本信息字段 ===
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='feedbacks',
        verbose_name='用户',
        help_text='提交反馈的用户'
    )
    feedback_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default='suggestion',
        verbose_name='反馈类型',
        help_text='反馈的类型分类'
    )
    title = models.CharField(
        max_length=200,
        verbose_name='标题',
        help_text='反馈的标题摘要'
    )
    content = models.TextField(
        verbose_name='反馈内容',
        help_text='反馈的详细内容'
    )
    images = models.JSONField(
        blank=True,
        null=True,
        verbose_name='图片列表',
        help_text='存储多张图片的URL列表，用于问题截图等'
    )
    contact_info = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='联系方式',
        help_text='用户的联系方式，便于跟进处理'
    )
    
    # === 关联关系 ===
    event = models.ForeignKey(
        'events.Event',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='feedbacks',
        verbose_name='关联赛事',
        help_text='如果是关于某个赛事的反馈，可关联具体赛事'
    )
    
    # === 处理状态和回复 ===
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='处理状态',
        help_text='反馈的处理状态'
    )
    reply = models.TextField(
        blank=True,
        null=True,
        verbose_name='回复内容',
        help_text='管理员对反馈的回复'
    )
    handler = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='handled_feedbacks',
        verbose_name='处理人',
        help_text='处理该反馈的管理员'
    )
    handled_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='处理时间',
        help_text='反馈处理完成的时间'
    )
    
    # === 匿名和时间 ===
    is_anonymous = models.BooleanField(
        default=False,
        verbose_name='是否匿名',
        help_text='匿名反馈不会显示用户的真实身份信息'
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
        # 数据库索引：优化查询性能
        indexes = [
            models.Index(fields=['status', '-created_at']),  # 按状态和时间查询
            models.Index(fields=['feedback_type']),          # 按类型查询
            models.Index(fields=['user']),                   # 按用户查询
        ]
    
    def __str__(self):
        """返回反馈的字符串表示"""
        return f"{self.user.username} - {self.title}"
