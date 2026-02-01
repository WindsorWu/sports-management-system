"""
互动应用序列化器（点赞、收藏、评论）
"""
from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from .models import Like, Favorite, Comment


class LikeSerializer(serializers.ModelSerializer):
    """点赞序列化器"""
    user_name = serializers.CharField(source='user.real_name', read_only=True)
    content_type_name = serializers.SerializerMethodField()

    class Meta:
        model = Like
        fields = ['id', 'user', 'user_name', 'content_type', 'content_type_name', 'object_id', 'created_at']
        read_only_fields = ['id', 'user', 'created_at', 'user_name', 'content_type_name']

    def get_content_type_name(self, obj):
        """获取内容类型名称"""
        return obj.content_type.model

    def create(self, validated_data):
        """创建点赞"""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class FavoriteSerializer(serializers.ModelSerializer):
    """收藏序列化器"""
    user_name = serializers.CharField(source='user.real_name', read_only=True)
    content_type_name = serializers.SerializerMethodField()
    object_id = serializers.IntegerField(write_only=True)
    target_id = serializers.IntegerField(source='object_id', read_only=True)
    event_name = serializers.SerializerMethodField()
    event_image = serializers.SerializerMethodField()
    event_type = serializers.SerializerMethodField()
    event_start_time = serializers.SerializerMethodField()

    class Meta:
        model = Favorite
        fields = [
            'id', 'user', 'user_name', 'content_type', 'content_type_name',
            'object_id', 'target_id', 'event_name', 'event_image', 'event_type',
            'event_start_time', 'remarks', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'user_name', 'content_type_name']

    def get_content_type_name(self, obj):
        """获取内容类型名称"""
        return obj.content_type.model

    def create(self, validated_data):
        """创建收藏"""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def get_event_name(self, obj):
        """获取事件名称"""
        return getattr(obj.content_object, 'title', None)

    def get_event_image(self, obj):
        """获取事件图片"""
        image_field = getattr(obj.content_object, 'cover_image', None)
        if not image_field:
            return None
        return image_field.url if hasattr(image_field, 'url') else image_field

    def get_event_type(self, obj):
        """获取事件类型"""
        return getattr(obj.content_object, 'event_type', None)

    def get_event_start_time(self, obj):
        """获取事件开始时间"""
        return getattr(obj.content_object, 'start_time', None)


class CommentSerializer(serializers.ModelSerializer):
    """评论序列化器"""
    user_name = serializers.CharField(source='user.real_name', read_only=True)
    user_avatar = serializers.ImageField(source='user.avatar', read_only=True)
    reply_to_name = serializers.CharField(source='reply_to.real_name', read_only=True)
    content_type_name = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id', 'user', 'user_name', 'user_avatar', 'content_type',
            'content_type_name', 'object_id', 'content', 'parent',
            'reply_to', 'reply_to_name', 'is_approved', 'like_count',
            'replies', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'user', 'like_count', 'created_at', 'updated_at',
            'user_name', 'user_avatar', 'reply_to_name', 'content_type_name', 'replies'
        ]

    def get_content_type_name(self, obj):
        """获取内容类型名称"""
        return obj.content_type.model

    def get_replies(self, obj):
        """获取回复列表"""
        if obj.replies.exists():
            return CommentSimpleSerializer(obj.replies.all(), many=True).data
        return []

    def create(self, validated_data):
        """创建评论"""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class CommentSimpleSerializer(serializers.ModelSerializer):
    """评论简单序列化器（用于回复列表，避免递归）"""
    user_name = serializers.CharField(source='user.real_name', read_only=True)
    user_avatar = serializers.ImageField(source='user.avatar', read_only=True)
    reply_to_name = serializers.CharField(source='reply_to.real_name', read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id', 'user', 'user_name', 'user_avatar', 'content',
            'reply_to', 'reply_to_name', 'is_approved', 'like_count',
            'created_at', 'updated_at'
        ]


class CommentCreateSerializer(serializers.ModelSerializer):
    """评论创建序列化器"""

    class Meta:
        model = Comment
        fields = ['content_type', 'object_id', 'content', 'parent', 'reply_to']

    def validate(self, attrs):
        """验证评论信息"""
        parent = attrs.get('parent')
        reply_to = attrs.get('reply_to')

        # 如果有父评论，验证父评论的内容类型和对象ID是否一致
        if parent:
            if parent.content_type != attrs.get('content_type') or parent.object_id != attrs.get('object_id'):
                raise serializers.ValidationError("父评论与当前评论的对象不匹配")

        # 如果有回复对象，验证回复对象是否是父评论的作者
        if parent and reply_to:
            if parent.user != reply_to:
                raise serializers.ValidationError("回复对象与父评论作者不匹配")

        return attrs

    def create(self, validated_data):
        """创建评论"""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
