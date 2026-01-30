"""
反馈应用序列化器
"""
from rest_framework import serializers
from .models import Feedback


class FeedbackSerializer(serializers.ModelSerializer):
    """反馈序列化器"""
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
    """反馈创建序列化器（简化版）"""

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
    """反馈列表序列化器（简化版）"""
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
    """反馈回复序列化器"""
    reply = serializers.CharField(required=True)
    status = serializers.ChoiceField(
        choices=Feedback.STATUS_CHOICES,
        default='resolved'
    )
