"""
公告应用序列化器

提供公告数据的序列化和反序列化功能，支持公告创建、查询等业务逻辑
"""
from rest_framework import serializers
from django.utils import timezone
from .models import Announcement


class AnnouncementSerializer(serializers.ModelSerializer):
    """
    公告序列化器
    
    用于公告数据的完整序列化，包含所有字段和关联信息
    
    主要功能:
        - 序列化公告完整信息
        - 包含作者、赛事等关联信息
        - 支持公告创建和更新
        - 自动设置发布时间
        
    扩展字段说明:
        - author_name: 发布者的真实姓名
        - author_username: 发布者的用户名
        - event_title: 关联赛事的标题
        - image: 封面图片路径（兼容性字段）
        - status: 发布状态（published/draft）
        
    使用场景:
        - 公告详情展示
        - 公告创建和编辑
        - 管理后台使用
    """
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
        """
        创建公告时自动设置作者和发布时间
        
        业务逻辑:
            - 自动设置作者为当前登录用户
            - 如果设置为发布且没有发布时间，自动设置为当前时间
        """
        validated_data['author'] = self.context['request'].user
        # 如果设置为发布，自动设置发布时间
        if validated_data.get('is_published') and not validated_data.get('publish_time'):
            validated_data['publish_time'] = timezone.now()
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        更新公告
        
        业务逻辑:
            - 如果从未发布改为发布，自动设置发布时间
        """
        # 如果从未发布改为发布，设置发布时间
        if validated_data.get('is_published') and not instance.is_published:
            if not validated_data.get('publish_time'):
                validated_data['publish_time'] = timezone.now()
        return super().update(instance, validated_data)

    def to_internal_value(self, data):
        """
        处理前端传入的status字段
        
        将status字段转换为is_published字段
        支持前端使用status='published'或'draft'的方式
        """
        data = data.copy()
        status_value = data.pop('status', None)
        if status_value is not None:
            data['is_published'] = status_value == 'published'
        return super().to_internal_value(data)

    def get_status(self, obj):
        """将is_published转换为status字段，便于前端使用"""
        return 'published' if obj.is_published else 'draft'


class AnnouncementListSerializer(serializers.ModelSerializer):
    """
    公告列表序列化器（简化版）
    
    用于公告列表展示的精简序列化器
    
    主要功能:
        - 只包含列表展示必要的字段
        - 减少数据传输量
        - 提高列表查询性能
        
    使用场景:
        - 公告列表页面
        - 首页公告展示
        - 移动端列表
    """
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
        """将is_published转换为status字段"""
        return 'published' if obj.is_published else 'draft'


class AnnouncementDetailSerializer(serializers.ModelSerializer):
    """
    公告详情序列化器（完整版）
    
    用于公告详情展示的完整序列化器
    
    主要功能:
        - 包含所有字段和详细信息
        - 包含作者和赛事的详细信息
        - 适用于公告详情页面
        
    使用场景:
        - 公告详情页面
        - 公告查看页面
    """
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
        """获取作者详细信息"""
        return {
            'id': obj.author.id,
            'username': obj.author.username,
            'real_name': obj.author.real_name,
        }

    def get_event_info(self, obj):
        """获取赛事详细信息（如果有关联赛事）"""
        if obj.event:
            return {
                'id': obj.event.id,
                'title': obj.event.title,
                'status': obj.event.status,
            }
        return None
