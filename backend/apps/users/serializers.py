"""
用户应用序列化器
"""
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils.translation import gettext_lazy as _


class UserSerializer(serializers.ModelSerializer):
    """
    用户基础序列化器
    
    用于用户数据的序列化和反序列化，适用于列表展示和基本的增删改查操作
    包含用户的基本信息和状态字段
    
    只读字段:
        - id: 用户唯一标识
        - created_at: 创建时间
        - updated_at: 更新时间
        - is_verified: 实名认证状态
        - date_joined: 注册时间
    """

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'real_name', 'phone', 'user_type',
            'avatar', 'gender', 'birth_date', 'id_card', 'emergency_contact',
            'emergency_phone', 'organization', 'bio', 'is_verified',
            'is_active', 'is_staff', 'date_joined', 'created_at', 'updated_at'
        ]
        # 这些字段不允许通过API直接修改
        read_only_fields = ['id', 'created_at', 'updated_at', 'is_verified', 'date_joined']


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    用户注册序列化器
    
    专门用于处理新用户注册逻辑，包含密码验证、确认密码、
    手机号格式验证等功能
    
    特殊字段:
        - password: 密码字段，仅写入，不在响应中返回
        - password_confirm: 确认密码字段，用于二次验证
    
    验证规则:
        1. 密码必须符合Django的密码强度要求
        2. 两次输入的密码必须一致
        3. 手机号必须是11位数字
    """
    password = serializers.CharField(
        write_only=True,          # 只用于写入，不会在响应中返回
        required=True,            # 必填字段
        validators=[validate_password],  # 使用Django内置的密码强度验证
        style={'input_type': 'password'}  # 前端显示为密码输入框
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password_confirm',
            'real_name', 'phone', 'user_type'
        ]

    def validate(self, attrs):
        """
        对象级别的验证，检查两次输入的密码是否一致
        
        参数:
            attrs: 包含所有字段值的字典
            
        返回:
            dict: 验证通过后的数据字典
            
        异常:
            ValidationError: 当两次密码不一致时抛出
        """
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "两次密码不一致"})
        return attrs

    def validate_phone(self, value):
        """
        字段级别的验证，检查手机号格式是否正确
        
        验证规则：必须是11位数字
        
        参数:
            value: 手机号字符串
            
        返回:
            str: 验证通过后的手机号
            
        异常:
            ValidationError: 当手机号格式不正确时抛出
        """
        if len(value) != 11 or not value.isdigit():
            raise serializers.ValidationError("手机号格式不正确")
        return value

    def create(self, validated_data):
        """
        创建新用户
        
        处理流程:
            1. 移除确认密码字段（不需要存储）
            2. 如果用户类型是裁判，设置is_staff为True
            3. 使用create_user方法创建用户（会自动加密密码）
        
        参数:
            validated_data: 经过验证的数据字典
            
        返回:
            User: 新创建的用户对象
        """
        # 移除确认密码字段，不需要存入数据库
        validated_data.pop('password_confirm')
        # 裁判用户设置为staff，便于后台管理
        validated_data['is_staff'] = validated_data.get('user_type') == 'referee'
        # 使用create_user方法，会自动处理密码加密
        user = User.objects.create_user(**validated_data)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """
    用户个人信息序列化器（详细版本）
    
    用于获取当前登录用户的完整个人信息，包含更多的系统状态字段
    相比UserSerializer，增加了is_superuser等管理相关字段
    
    使用场景:
        GET /api/users/me/ - 获取当前用户的详细信息
        
    只读字段说明:
        - id: 用户ID，系统自动生成
        - username: 用户名，注册后不可修改
        - is_verified: 实名认证状态，需要管理员审核
        - is_active: 账号激活状态，管理员控制
        - is_superuser: 超级管理员标志，系统级权限
        - is_staff: 后台访问权限，通常给裁判和管理员
        - date_joined: 账号注册时间
        - created_at, updated_at: 记录创建和更新时间
    """

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'real_name', 'phone', 'user_type',
            'avatar', 'gender', 'birth_date', 'id_card', 'emergency_contact',
            'emergency_phone', 'organization', 'bio', 'is_verified',
            'is_active', 'is_superuser', 'is_staff',
            'date_joined', 'created_at', 'updated_at'
        ]
        # 这些字段只能查看，不能通过此序列化器修改
        read_only_fields = [
            'id', 'username', 'is_verified', 'is_active', 'is_superuser',
            'is_staff', 'date_joined', 'created_at', 'updated_at'
        ]


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """
    用户个人信息更新序列化器
    
    专门用于用户更新自己的个人基本信息
    只允许修改有限的几个字段：用户名、邮箱、手机号
    
    使用场景:
        PUT/PATCH /api/users/update_profile/ - 更新当前用户信息
        
    可修改字段:
        - username: 用户名，必填
        - email: 邮箱地址，必填
        - phone: 手机号，可选
    
    注意：此序列化器不包含敏感信息的修改，如密码、用户类型等
    """

    class Meta:
        model = User
        fields = ['username', 'email', 'phone']
        extra_kwargs = {
            'username': {'required': True},  # 用户名必填
            'email': {'required': True},     # 邮箱必填
            'phone': {'required': False}     # 手机号可选
        }


class ChangePasswordSerializer(serializers.Serializer):
    """
    修改密码序列化器
    
    用于处理用户修改密码的逻辑，需要验证旧密码并确认新密码
    不继承ModelSerializer，因为不涉及直接的模型字段映射
    
    使用场景:
        POST /api/users/change_password/
        
    字段说明:
        - old_password: 当前密码，用于验证用户身份
        - new_password: 新密码，必须符合密码强度要求
        - new_password_confirm: 确认新密码，必须与新密码一致
    
    验证流程:
        1. 检查旧密码是否正确
        2. 检查新密码是否符合强度要求
        3. 检查两次输入的新密码是否一致
    """
    old_password = serializers.CharField(
        required=True,
        write_only=True,                    # 只用于验证，不返回
        style={'input_type': 'password'}    # 前端显示为密码框
    )
    new_password = serializers.CharField(
        required=True,
        write_only=True,
        validators=[validate_password],      # 验证新密码强度
        style={'input_type': 'password'}
    )
    new_password_confirm = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )

    def validate(self, attrs):
        """
        对象级别验证：检查两次输入的新密码是否一致
        
        参数:
            attrs: 包含所有字段值的字典
            
        返回:
            dict: 验证通过后的数据字典
            
        异常:
            ValidationError: 当两次新密码不一致时抛出
        """
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({"new_password": "两次新密码不一致"})
        return attrs

    def validate_old_password(self, value):
        """
        字段级别验证：检查旧密码是否正确
        
        从上下文中获取当前用户，使用check_password方法验证密码
        
        参数:
            value: 用户输入的旧密码
            
        返回:
            str: 验证通过后的旧密码
            
        异常:
            ValidationError: 当旧密码不正确时抛出
        """
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("旧密码不正确")
        return value


class LoginSerializer(TokenObtainPairSerializer):
    """
    登录序列化器
    
    继承自JWT的TokenObtainPairSerializer，用于处理用户登录逻辑
    返回JWT访问令牌和刷新令牌
    
    自定义错误消息:
        - no_active_account: 当用户名或密码错误时，显示中文友好提示
        
    使用场景:
        POST /api/token/ - 用户登录获取token
        
    返回数据:
        {
            "access": "访问令牌（有效期较短）",
            "refresh": "刷新令牌（用于获取新的访问令牌）"
        }
    """
    # 自定义错误消息，覆盖父类的默认英文消息
    default_error_messages = {
        **TokenObtainPairSerializer.default_error_messages,
        'no_active_account': _('用户名或密码错误')  # 使用国际化翻译
    }
