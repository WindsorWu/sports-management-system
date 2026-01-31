"""
用户应用序列化器
"""
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """用户序列化器"""

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'real_name', 'phone', 'user_type',
            'avatar', 'gender', 'birth_date', 'id_card', 'emergency_contact',
            'emergency_phone', 'organization', 'bio', 'is_verified',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'is_verified']


class UserRegisterSerializer(serializers.ModelSerializer):
    """用户注册序列化器"""
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
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
        """验证密码是否一致"""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "两次密码不一致"})
        return attrs

    def validate_phone(self, value):
        """验证手机号格式"""
        if len(value) != 11 or not value.isdigit():
            raise serializers.ValidationError("手机号格式不正确")
        return value

    def create(self, validated_data):
        """创建用户"""
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """用户个人信息序列化器（更详细）"""

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'real_name', 'phone', 'user_type',
            'avatar', 'gender', 'birth_date', 'id_card', 'emergency_contact',
            'emergency_phone', 'organization', 'bio', 'is_verified',
            'is_active', 'is_superuser', 'date_joined', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'username', 'is_verified', 'is_active', 'is_superuser',
            'date_joined', 'created_at', 'updated_at'
        ]


class ChangePasswordSerializer(serializers.Serializer):
    """修改密码序列化器"""
    old_password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )
    new_password = serializers.CharField(
        required=True,
        write_only=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    new_password_confirm = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )

    def validate(self, attrs):
        """验证新密码是否一致"""
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({"new_password": "两次新密码不一致"})
        return attrs

    def validate_old_password(self, value):
        """验证旧密码是否正确"""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("旧密码不正确")
        return value
