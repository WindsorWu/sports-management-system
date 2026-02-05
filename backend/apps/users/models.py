from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    用户模型
    
    继承自Django的AbstractUser，扩展了用户的基本信息字段
    支持多种用户角色：运动员、组织者、裁判、管理员
    
    主要功能:
        - 用户注册和认证
        - 角色权限管理
        - 个人信息管理
        - 实名认证
        
    数据表名: user
    """
    # 重写username字段，移除默认的验证器
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer.'),
        validators=[],  # 移除默认验证器，允许更灵活的用户名格式
        error_messages={
            'unique': _('A user with that username already exists.'),
        },
    )
    
    # 用户类型选项：定义系统支持的四种用户角色
    USER_TYPE_CHOICES = (
        ('athlete', '运动员'),      # 普通参赛者
        ('organizer', '组织者'),    # 赛事组织方
        ('referee', '裁判'),        # 裁判员，负责成绩录入和审核
        ('admin', '管理员'),        # 系统管理员
    )
    
    # 性别选项
    GENDER_CHOICES = (
        ('M', '男'),
        ('F', '女'),
        ('O', '其他'),
    )
    
    # === 基本信息字段 ===
    real_name = models.CharField(
        max_length=50,
        verbose_name='真实姓名',
        help_text='用户真实姓名'
    )
    phone = models.CharField(
        max_length=11,
        unique=True,                # 手机号必须唯一，可用于登录
        verbose_name='手机号',
        help_text='11位手机号码'
    )
    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default='athlete',          # 默认为运动员角色
        verbose_name='用户类型',
        help_text='用户角色类型'
    )
    avatar = models.ImageField(
        upload_to='avatars/%Y/%m/',  # 按年月组织头像文件
        blank=True,
        null=True,
        verbose_name='头像',
        help_text='用户头像图片'
    )
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        blank=True,
        null=True,
        verbose_name='性别'
    )
    birth_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='出生日期'
    )
    
    # === 身份认证信息 ===
    id_card = models.CharField(
        max_length=18,
        blank=True,
        null=True,
        unique=True,                # 身份证号唯一，用于实名认证
        verbose_name='身份证号',
        help_text='18位身份证号码'
    )
    
    # === 紧急联系人信息 ===
    emergency_contact = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='紧急联系人'
    )
    emergency_phone = models.CharField(
        max_length=11,
        blank=True,
        null=True,
        verbose_name='紧急联系电话'
    )
    
    # === 其他信息 ===
    organization = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='所属组织',
        help_text='学校、单位等'
    )
    bio = models.TextField(
        blank=True,
        null=True,
        verbose_name='个人简介'
    )
    
    # === 状态字段 ===
    is_verified = models.BooleanField(
        default=False,
        verbose_name='是否实名认证'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,          # 创建时自动设置
        verbose_name='创建时间'
    )
    updated_at = models.DateTimeField(
        auto_now=True,              # 每次更新时自动更新
        verbose_name='更新时间'
    )
    
    class Meta:
        db_table = 'user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']  # 默认按创建时间倒序排列
    
    def __str__(self):
        """
        字符串表示方法
        返回格式: "用户名 (真实姓名)"
        """
        return f"{self.username} ({self.real_name})"
