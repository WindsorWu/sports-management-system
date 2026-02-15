from django.db import models
from django.conf import settings


class Registration(models.Model):
    """
    报名模型
    
    存储用户对赛事的报名信息，包括参赛者信息、审核状态、支付信息等
    
    主要功能:
        - 赛事报名管理：记录用户报名信息和参赛者详情
        - 审核流程：支持待审核、已通过、已拒绝、已取消四种状态
        - 支付管理：跟踪报名费用的支付状态
        - 唯一性约束：同一用户对同一赛事只能报名一次
        
    业务逻辑:
        - 报名时自动生成唯一报名编号(格式: REG-赛事ID-时间戳-随机码)
        - 报名成功后增加赛事的当前报名人数
        - 取消或拒绝报名时减少赛事的报名人数
        - 需要填写参赛者个人信息和紧急联系人
        
    关键字段说明:
        - status: 审核状态，影响是否允许参赛
        - payment_status: 支付状态，与报名费用关联
        - registration_number: 报名编号，系统自动生成，全局唯一
        
    数据表名: registration
    """
    # 报名审核状态选项
    STATUS_CHOICES = (
        ('pending', '待审核'),      # 刚提交报名，等待审核
        ('approved', '已通过'),     # 审核通过，允许参赛
        ('rejected', '已拒绝'),     # 审核未通过，不允许参赛
        ('cancelled', '已取消'),    # 用户主动取消报名
    )
    
    # 报名费支付状态选项
    PAYMENT_STATUS_CHOICES = (
        ('unpaid', '未支付'),      # 尚未支付报名费
        ('paid', '已支付'),        # 已完成支付
        ('refunded', '已退款'),    # 已退还报名费
    )
    
    # === 关联字段 ===
    event = models.ForeignKey(
        'events.Event',
        on_delete=models.CASCADE,
        related_name='registrations',  # 反向查询: event.registrations.all()
        verbose_name='赛事'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='registrations',  # 反向查询: user.registrations.all()
        verbose_name='用户',
        help_text='提交报名的用户'
    )
    
    # === 报名状态字段 ===
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='审核状态',
        help_text='报名的审核状态，影响是否允许参赛'
    )
    registration_number = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='报名编号',
        help_text='系统自动生成的唯一报名编号，格式: REG-赛事ID-时间戳-随机码'
    )
    
    # === 参赛者基本信息字段 ===
    participant_name = models.CharField(
        max_length=50,
        verbose_name='参赛者姓名',
        help_text='实际参赛人员的真实姓名'
    )
    participant_phone = models.CharField(
        max_length=11,
        verbose_name='参赛者电话',
        help_text='参赛者联系电话，11位手机号'
    )
    participant_id_card = models.CharField(
        max_length=18,
        verbose_name='参赛者身份证',
        help_text='参赛者身份证号码，用于实名认证'
    )
    participant_gender = models.CharField(
        max_length=1,
        choices=(('M', '男'), ('F', '女'), ('O', '其他')),
        verbose_name='参赛者性别'
    )
    participant_birth_date = models.DateField(
        verbose_name='参赛者出生日期',
        help_text='用于年龄验证和分组'
    )
    participant_organization = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='参赛者单位',
        help_text='参赛者所属单位或组织（可选）'
    )
    
    # === 紧急联系人信息 ===
    emergency_contact = models.CharField(
        max_length=50,
        verbose_name='紧急联系人',
        help_text='紧急情况下的联系人姓名'
    )
    emergency_phone = models.CharField(
        max_length=11,
        verbose_name='紧急联系电话',
        help_text='紧急联系人的手机号码'
    )
    
    # === 支付相关字段 ===
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='unpaid',
        verbose_name='支付状态',
        help_text='报名费的支付状态'
    )
    payment_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name='支付金额',
        help_text='需要支付的报名费用，单位：元'
    )
    payment_time = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='支付时间',
        help_text='完成支付的具体时间'
    )
    
    # === 备注信息 ===
    remarks = models.TextField(
        blank=True,
        null=True,
        verbose_name='备注信息',
        help_text='用户提交报名时的补充说明'
    )
    
    # === 审核相关字段 ===
    review_remarks = models.TextField(
        blank=True,
        null=True,
        verbose_name='审核备注',
        help_text='审核人员填写的审核意见或拒绝原因'
    )
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_registrations',  # 反向查询: user.reviewed_registrations.all()
        verbose_name='审核人',
        help_text='执行审核操作的管理员或组织者'
    )
    reviewed_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='审核时间',
        help_text='完成审核的具体时间'
    )
    
    # === 时间戳字段 ===
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='报名时间',
        help_text='用户提交报名的时间'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='更新时间',
        help_text='报名信息最后修改的时间'
    )
    
    class Meta:
        db_table = 'registration'
        verbose_name = '报名'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']  # 默认按报名时间倒序排列，最新的在前
        unique_together = [['event', 'user']]  # 联合唯一约束：同一用户对同一赛事只能报名一次
        indexes = [
            # 为常用查询字段添加索引，提高查询性能
            models.Index(fields=['status']),  # 按审核状态查询
            models.Index(fields=['registration_number']),  # 按报名编号查询
            models.Index(fields=['event', 'user']),  # 联合索引，用于唯一性检查
        ]
    
    def __str__(self):
        """返回报名的字符串表示"""
        return f"{self.participant_name} - {self.event.title}"
