from django.db import models
from django.conf import settings


class Registration(models.Model):
    """报名模型"""
    STATUS_CHOICES = (
        ('pending', '待审核'),
        ('approved', '已通过'),
        ('rejected', '已拒绝'),
        ('cancelled', '已取消'),
    )
    
    PAYMENT_STATUS_CHOICES = (
        ('unpaid', '未支付'),
        ('paid', '已支付'),
        ('refunded', '已退款'),
    )
    
    event = models.ForeignKey(
        'events.Event',
        on_delete=models.CASCADE,
        related_name='registrations',
        verbose_name='赛事'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='registrations',
        verbose_name='用户'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='审核状态'
    )
    registration_number = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='报名编号',
        help_text='系统自动生成'
    )
    participant_name = models.CharField(
        max_length=50,
        verbose_name='参赛者姓名'
    )
    participant_phone = models.CharField(
        max_length=11,
        verbose_name='参赛者电话'
    )
    participant_id_card = models.CharField(
        max_length=18,
        verbose_name='参赛者身份证'
    )
    participant_gender = models.CharField(
        max_length=1,
        choices=(('M', '男'), ('F', '女'), ('O', '其他')),
        verbose_name='参赛者性别'
    )
    participant_birth_date = models.DateField(
        verbose_name='参赛者出生日期'
    )
    participant_organization = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='参赛者单位'
    )
    emergency_contact = models.CharField(
        max_length=50,
        verbose_name='紧急联系人'
    )
    emergency_phone = models.CharField(
        max_length=11,
        verbose_name='紧急联系电话'
    )
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='unpaid',
        verbose_name='支付状态'
    )
    payment_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='支付金额'
    )
    payment_time = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='支付时间'
    )
    remarks = models.TextField(
        blank=True,
        null=True,
        verbose_name='备注信息'
    )
    review_remarks = models.TextField(
        blank=True,
        null=True,
        verbose_name='审核备注'
    )
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_registrations',
        verbose_name='审核人'
    )
    reviewed_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='审核时间'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='报名时间'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='更新时间'
    )
    
    class Meta:
        db_table = 'registration'
        verbose_name = '报名'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
        unique_together = [['event', 'user']]
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['registration_number']),
            models.Index(fields=['event', 'user']),
        ]
    
    def __str__(self):
        return f"{self.participant_name} - {self.event.title}"
