"""
反馈应用序列化器

提供反馈数据的序列化和反序列化功能
"""
from rest_framework import serializers
from .models import Feedback


class FeedbackSerializer(serializers.ModelSerializer):
    """
    反馈序列化器
    
    用于反馈数据的完整序列化
    
    主要功能:
        - 序列化反馈完整信息
        - 包含用户、赛事、处理人信息
        - 自动设置反馈用户
        - 匿名反馈保护
    """
    user_name = serializers.CharField(source='user.real_name', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    event_title = serializers.CharField(source='event.title', read_only=True)
    handler_name = serializers.CharField(source='handler.real_name', read_only=True)

    class Meta:
        model = Feedback
        fields = [
            'id', 'user', 'user_name', 'user_username', 'feedback_type',
            'title', 'content', 'images', 'contact_info', 'event', 'event_title',
            'status', 'reply', 'handler', 'handler_name', 'handled_at',
            'is_anonymous', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'user', 'handler', 'handled_at', 'created_at', 'updated_at',
            'user_name', 'user_username', 'event_title', 'handler_name'
        ]

    def create(self, validated_data):
        """创建反馈时自动设置用户"""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def to_representation(self, instance):
        """如果是匿名反馈，隐藏用户信息"""
        data = super().to_representation(instance)
        if instance.is_anonymous:
            data['user_name'] = '匿名用户'
            data['user_username'] = 'anonymous'
        return data


class FeedbackCreateSerializer(serializers.ModelSerializer):
    """
    反馈创建序列化器（简化版）
    
    用于用户提交反馈
    只包含用户需要填写的字段
    """

    class Meta:
        model = Feedback
        fields = [
            'feedback_type', 'title', 'content', 'images',
            'contact_info', 'event', 'is_anonymous'
        ]

    def create(self, validated_data):
        """创建反馈时自动设置用户"""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class FeedbackListSerializer(serializers.ModelSerializer):
    """
    反馈列表序列化器（简化版）
    
    用于反馈列表展示
    只包含列表必要的字段
    """
    user_name = serializers.SerializerMethodField()
    event_title = serializers.CharField(source='event.title', read_only=True)

    class Meta:
        model = Feedback
        fields = [
            'id', 'user_name', 'feedback_type', 'title',
            'event_title', 'status', 'is_anonymous', 'created_at'
        ]

    def get_user_name(self, obj):
        """如果是匿名反馈，返回匿名用户"""
        if obj.is_anonymous:
            return '匿名用户'
        return obj.user.real_name


class FeedbackReplySerializer(serializers.Serializer):
    """
    反馈回复序列化器
    
    用于管理员回复反馈
    
    字段说明:
        - reply: 回复内容（必填）
        - status: 处理状态（可选，默认为已解决）
    """
    reply = serializers.CharField(required=True)
    status = serializers.ChoiceField(
        choices=Feedback.STATUS_CHOICES,
        default='resolved'
    )
