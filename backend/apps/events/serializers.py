"""
赛事应用序列化器
"""
from rest_framework import serializers
from .models import Event


class EventSerializer(serializers.ModelSerializer):
    """赛事序列化器"""
    organizer_name = serializers.CharField(source='organizer.real_name', read_only=True)
    organizer_username = serializers.CharField(source='organizer.username', read_only=True)

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'cover_image', 'event_type', 'level',
            'status', 'location', 'start_time', 'end_time', 'registration_start',
            'registration_end', 'max_participants', 'current_participants',
            'registration_fee', 'rules', 'requirements', 'prizes', 'organizer',
            'organizer_name', 'organizer_username', 'contact_person',
            'contact_phone', 'contact_email', 'view_count', 'is_featured',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'organizer', 'current_participants', 'view_count',
            'created_at', 'updated_at', 'organizer_name', 'organizer_username'
        ]

    def create(self, validated_data):
        """创建赛事时自动设置组织者"""
        validated_data['organizer'] = self.context['request'].user
        return super().create(validated_data)


class EventListSerializer(serializers.ModelSerializer):
    """赛事列表序列化器（简化版）"""
    organizer_name = serializers.CharField(source='organizer.real_name', read_only=True)

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'cover_image', 'event_type', 'level', 'status',
            'location', 'start_time', 'end_time', 'registration_start',
            'registration_end', 'max_participants', 'current_participants',
            'registration_fee', 'organizer_name', 'view_count', 'is_featured',
            'created_at'
        ]


class EventDetailSerializer(serializers.ModelSerializer):
    """赛事详情序列化器（完整版）"""
    organizer_info = serializers.SerializerMethodField()
    registration_count = serializers.IntegerField(source='current_participants', read_only=True)
    can_register = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'cover_image', 'event_type', 'level',
            'status', 'location', 'start_time', 'end_time', 'registration_start',
            'registration_end', 'max_participants', 'current_participants',
            'registration_count', 'registration_fee', 'rules', 'requirements',
            'prizes', 'organizer', 'organizer_info', 'contact_person',
            'contact_phone', 'contact_email', 'view_count', 'is_featured',
            'can_register', 'created_at', 'updated_at'
        ]

    def get_organizer_info(self, obj):
        """获取组织者信息"""
        return {
            'id': obj.organizer.id,
            'username': obj.organizer.username,
            'real_name': obj.organizer.real_name,
            'organization': obj.organizer.organization,
        }

    def get_can_register(self, obj):
        """判断是否可以报名"""
        from django.utils import timezone
        now = timezone.now()

        # 检查报名时间
        if now < obj.registration_start or now > obj.registration_end:
            return False

        # 检查赛事状态
        if obj.status not in ['published', 'ongoing']:
            return False

        # 检查人数限制
        if obj.max_participants > 0 and obj.current_participants >= obj.max_participants:
            return False

        return True
