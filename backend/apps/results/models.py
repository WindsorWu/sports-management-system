from django.db import models
from django.conf import settings


class Result(models.Model):
    """成绩模型"""
    STATUS_CHOICES = (
        ('preliminary', '初赛'),
        ('semifinal', '半决赛'),
        ('final', '决赛'),
    )
    
    event = models.ForeignKey(
        'events.Event',
        on_delete=models.CASCADE,
        related_name='results',
        verbose_name='赛事'
    )
    registration = models.ForeignKey(
        'registrations.Registration',
        on_delete=models.CASCADE,
        related_name='results',
        verbose_name='报名记录'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='results',
        verbose_name='用户'
    )
    round_type = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='final',
        verbose_name='轮次'
    )
    score = models.CharField(
        max_length=100,
        verbose_name='成绩',
        help_text='可以是时间、分数、距离等'
    )
    rank = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='排名'
    )
    award = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='奖项',
        help_text='如：金牌、银牌、铜牌、一等奖等'
    )
    score_unit = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='成绩单位',
        help_text='如：秒、分、米等'
    )
    remarks = models.TextField(
        blank=True,
        null=True,
        verbose_name='备注'
    )
    certificate_url = models.URLField(
        blank=True,
        null=True,
        verbose_name='证书链接',
        help_text='电子证书URL'
    )
    is_published = models.BooleanField(
        default=False,
        verbose_name='是否公开',
        help_text='是否公开显示成绩'
    )
    recorded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='recorded_results',
        verbose_name='录入人'
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
        db_table = 'result'
        verbose_name = '成绩'
        verbose_name_plural = verbose_name
        ordering = ['event', 'rank']
        indexes = [
            models.Index(fields=['event', 'rank']),
            models.Index(fields=['user']),
            models.Index(fields=['is_published']),
        ]
    
    def __str__(self):
        return f"{self.user.real_name} - {self.event.title} - {self.score}"
