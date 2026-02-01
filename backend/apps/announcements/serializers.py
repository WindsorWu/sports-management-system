"""
公告应用序列化器
"""
from rest_framework import serializers
from django.utils import timezone
from .models import Announcement


class AnnouncementSerializer(serializers.ModelSerializer):
    """公告序列化器"""
    author_name = serializers.CharField(source='author.real_name', read_only=True)
    author_username = serializers.CharField(source='author.username', read_only=True)
    event_title = serializers.CharField(source='event.title', read_only=True)
    image = serializers.CharField(source='cover_image', required=False, allow_null=True)
    status = serializers.SerializerMethodField()

    class Meta:
        model = Announcement
        fields = [
            'id', 'title', 'content', 'summary', 'announcement_type', 'priority',
            'event', 'event_title', 'cover_image', 'image', 'attachments', 'author',
            'author_name', 'author_username', 'is_published', 'is_pinned',
            'view_count', 'publish_time', 'expire_time', 'created_at', 'updated_at', 'status'
        ]
        read_only_fields = [
            'id', 'author', 'view_count', 'created_at', 'updated_at',
            'author_name', 'author_username', 'event_title'
        ]

    def create(self, validated_data):
        """创建公告时自动设置作者"""
        validated_data['author'] = self.context['request'].user
        # 如果设置为发布，自动设置发布时间
        if validated_data.get('is_published') and not validated_data.get('publish_time'):
            validated_data['publish_time'] = timezone.now()
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """更新公告"""
        # 如果从未发布改为发布，设置发布时间
        if validated_data.get('is_published') and not instance.is_published:
            if not validated_data.get('publish_time'):
                validated_data['publish_time'] = timezone.now()
        return super().update(instance, validated_data)

    def to_internal_value(self, data):
        data = data.copy()
        status_value = data.pop('status', None)
        if status_value is not None:
            data['is_published'] = status_value == 'published'
        return super().to_internal_value(data)

    def get_status(self, obj):
        return 'published' if obj.is_published else 'draft'


class AnnouncementListSerializer(serializers.ModelSerializer):
    """公告列表序列化器（简化版）"""
    author_name = serializers.CharField(source='author.real_name', read_only=True)
    event_title = serializers.CharField(source='event.title', read_only=True)
    status = serializers.SerializerMethodField()
    image = serializers.CharField(source='cover_image', read_only=True, allow_null=True)

    class Meta:
        model = Announcement
        fields = [
            'id', 'title', 'summary', 'announcement_type', 'priority', 'event_title',
            'cover_image', 'image', 'author_name', 'is_published', 'is_pinned',
            'view_count', 'publish_time', 'created_at', 'status'
        ]

    def get_status(self, obj):
        return 'published' if obj.is_published else 'draft'


class AnnouncementDetailSerializer(serializers.ModelSerializer):
    """公告详情序列化器（完整版）"""
    author_info = serializers.SerializerMethodField()
    event_info = serializers.SerializerMethodField()
    image = serializers.CharField(source='cover_image', read_only=True, allow_null=True)

    class Meta:
        model = Announcement
        fields = [
            'id', 'title', 'content', 'summary', 'announcement_type', 'priority',
            'event', 'event_info', 'cover_image', 'image', 'attachments', 'author',
            'author_info', 'is_published', 'is_pinned', 'view_count',
            'publish_time', 'expire_time', 'created_at', 'updated_at'
        ]

    def get_author_info(self, obj):
        """获取作者信息"""
        return {
            'id': obj.author.id,
            'username': obj.author.username,
            'real_name': obj.author.real_name,
        }

    def get_event_info(self, obj):
        """获取赛事信息"""
        if obj.event:
            return {
                'id': obj.event.id,
                'title': obj.event.title,
                'status': obj.event.status,
            }
        return None
