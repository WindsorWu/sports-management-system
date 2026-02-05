from django.db import models
from django.conf import settings


class Result(models.Model):
    """
    成绩模型
    
    存储运动员在赛事中的比赛成绩和排名信息
    
    主要功能:
        - 记录运动员的比赛成绩（时间、分数、距离等）
        - 记录排名和奖项信息
        - 支持多轮次比赛（初赛、半决赛、决赛）
        - 成绩公开状态控制
        - 电子证书管理
        
    关键字段说明:
        - score: 成绩值，可以是时间、分数、距离等，根据项目类型灵活填写
        - rank: 排名，用于生成排行榜
        - round_type: 比赛轮次，支持初赛、半决赛、决赛
        - is_published: 是否公开，未公开前运动员看不到成绩
        - award: 获得的奖项，如金牌、银牌、一等奖等
        - certificate_url: 电子证书链接
        
    使用场景:
        - 裁判录入比赛成绩
        - 生成排行榜
        - 运动员查看个人成绩
        - 导出成绩单
        
    数据表名: result
    """
    # 比赛轮次选项
    STATUS_CHOICES = (
        ('preliminary', '初赛'),    # 预赛/初赛，第一轮比赛
        ('semifinal', '半决赛'),     # 半决赛，淘汰赛中间轮次
        ('final', '决赛'),          # 决赛，最终轮次
    )
    
    # === 关联关系字段 ===
    event = models.ForeignKey(
        'events.Event',
        on_delete=models.CASCADE,
        related_name='results',
        verbose_name='赛事',
        help_text='关联的赛事，成绩属于哪个赛事'
    )
    registration = models.ForeignKey(
        'registrations.Registration',
        on_delete=models.CASCADE,
        related_name='results',
        verbose_name='报名记录',
        help_text='关联的报名记录，必须是已审核通过的报名'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='results',
        verbose_name='用户',
        help_text='参赛运动员，从报名记录自动获取'
    )
    
    # === 成绩信息字段 ===
    round_type = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='final',
        verbose_name='轮次',
        help_text='比赛轮次：初赛、半决赛或决赛'
    )
    score = models.CharField(
        max_length=100,
        verbose_name='成绩',
        help_text='成绩值，可以是时间、分数、距离等，如: 10.23、85分、5.6米'
    )
    rank = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='排名',
        help_text='该轮次的排名，用于生成排行榜'
    )
    award = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='奖项',
        help_text='获得的奖项，如：金牌、银牌、铜牌、一等奖等'
    )
    score_unit = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='成绩单位',
        help_text='成绩单位，如：秒、分、米、kg等'
    )
    remarks = models.TextField(
        blank=True,
        null=True,
        verbose_name='备注',
        help_text='成绩备注，可记录特殊情况或说明'
    )
    
    # === 证书和公开状态 ===
    certificate_url = models.URLField(
        blank=True,
        null=True,
        verbose_name='证书链接',
        help_text='电子证书的URL地址'
    )
    is_published = models.BooleanField(
        default=False,
        verbose_name='是否公开',
        help_text='是否公开显示成绩。未公开前运动员看不到成绩'
    )
    
    # === 审计字段 ===
    recorded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='recorded_results',
        verbose_name='录入人',
        help_text='录入成绩的裁判或管理员'
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
        # 默认排序：先按赛事，再按排名（排名小的在前）
        ordering = ['event', 'rank']
        # 数据库索引：优化查询性能
        indexes = [
            models.Index(fields=['event', 'rank']),      # 按赛事和排名查询
            models.Index(fields=['user']),               # 按用户查询个人成绩
            models.Index(fields=['is_published']),       # 按公开状态过滤
        ]
    
    def __str__(self):
        """返回成绩的字符串表示"""
        return f"{self.user.real_name} - {self.event.title} - {self.score}"
