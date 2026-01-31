from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """用户模型"""
    USER_TYPE_CHOICES = (
        ('athlete', '运动员'),
        ('organizer', '组织者'),
        ('referee', '裁判'),
        ('admin', '管理员'),
    )
    
    GENDER_CHOICES = (
        ('M', '男'),
        ('F', '女'),
        ('O', '其他'),
    )
    
    real_name = models.CharField(
        max_length=50,
        verbose_name='真实姓名',
        help_text='用户真实姓名'
    )
    phone = models.CharField(
        max_length=11,
        unique=True,
        verbose_name='手机号',
        help_text='11位手机号码'
    )
    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default='athlete',
        verbose_name='用户类型',
        help_text='用户角色类型'
    )
    avatar = models.ImageField(
        upload_to='avatars/%Y/%m/',
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
    id_card = models.CharField(
        max_length=18,
        blank=True,
        null=True,
        unique=True,
        verbose_name='身份证号',
        help_text='18位身份证号码'
    )
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
    is_verified = models.BooleanField(
        default=False,
        verbose_name='是否实名认证'
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
        db_table = 'user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.username} ({self.real_name})"
