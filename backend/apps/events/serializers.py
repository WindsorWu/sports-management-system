"""
赛事应用序列化器
"""
from rest_framework import serializers
from .models import Event, EventAssignment, RefereeEventAccess
from apps.interactions.models import Favorite


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
    is_registered = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    display_status = serializers.SerializerMethodField()

    # 添加字段别名以兼容前端
    name = serializers.CharField(source='title', read_only=True)
    image = serializers.CharField(source='cover_image', read_only=True)
    event_time = serializers.DateTimeField(source='start_time', read_only=True)
    registration_start_time = serializers.DateTimeField(source='registration_start', read_only=True)
    registration_end_time = serializers.DateTimeField(source='registration_end', read_only=True)
    registration_count = serializers.SerializerMethodField()
    click_count = serializers.IntegerField(source='view_count', read_only=True)

    class Meta:
        model = Event
        fields = [
            # 原有字段
            'id', 'title', 'cover_image', 'event_type', 'level', 'status',
            'location', 'start_time', 'end_time', 'registration_start',
            'registration_end', 'max_participants', 'current_participants',
            'registration_fee', 'organizer_name', 'view_count', 'is_featured',
            'description',
            'created_at',
            # 新增字段别名
            'name', 'image', 'event_time', 'registration_start_time',
            'registration_end_time', 'registration_count', 'click_count',
            # 联系人字段
            'contact_person', 'contact_phone',
            # 用户状态字段
            'is_registered', 'is_liked', 'is_favorited',
            # 动态状态字段
            'display_status'
        ]

    def get_is_registered(self, obj):
        """判断当前用户是否已报名"""
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False

        from apps.registrations.models import Registration
        return Registration.objects.filter(
            event=obj,
            user=request.user,
            status__in=['pending', 'approved']
        ).exists()

    def get_is_liked(self, obj):
        """判断当前用户是否已点赞"""
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False

        from apps.interactions.models import Like
        return Like.objects.filter(
            user=request.user,
            content_type__model='event',
            object_id=obj.id
        ).exists()

    def get_is_favorited(self, obj):
        """判断当前用户是否已收藏"""
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False

        return Favorite.objects.filter(
            user=request.user,
            content_type__model='event',
            object_id=obj.id
        ).exists()

    def get_display_status(self, obj):
        """展示用动态状态"""
        return obj.display_status

    def get_registration_count(self, obj):
        count = getattr(obj, 'approved_registration_count', None)
        if count is not None:
            return count
        return obj.registrations.filter(status='approved').count()


class EventDetailSerializer(serializers.ModelSerializer):
    """赛事详情序列化器（完整版）"""
    organizer_info = serializers.SerializerMethodField()
    registration_count = serializers.SerializerMethodField()
    can_register = serializers.SerializerMethodField()
    is_registered = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    display_status = serializers.SerializerMethodField()

    # 添加字段别名以兼容前端
    name = serializers.CharField(source='title', read_only=True)
    image = serializers.CharField(source='cover_image', read_only=True)
    registration_start_time = serializers.DateTimeField(source='registration_start', read_only=True)
    registration_end_time = serializers.DateTimeField(source='registration_end', read_only=True)
    click_count = serializers.IntegerField(source='view_count', read_only=True)

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'cover_image', 'event_type', 'level',
            'status', 'location', 'start_time', 'end_time', 'registration_start',
            'registration_end', 'max_participants', 'current_participants',
            'registration_count', 'registration_fee', 'rules', 'requirements',
            'prizes', 'organizer', 'organizer_info', 'contact_person',
            'contact_phone', 'contact_email', 'view_count', 'is_featured',
            'can_register', 'is_registered', 'is_liked', 'is_favorited',
            'created_at', 'updated_at',
            # 字段别名
            'name', 'image', 'registration_start_time', 'registration_end_time',
            'click_count', 'display_status'
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

    def get_is_registered(self, obj):
        """判断当前用户是否已报名"""
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False

        from apps.registrations.models import Registration
        return Registration.objects.filter(
            event=obj,
            user=request.user,
            status__in=['pending', 'approved']
        ).exists()

    def get_is_liked(self, obj):
        """判断当前用户是否已点赞"""
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False

        from apps.interactions.models import Like
        return Like.objects.filter(
            user=request.user,
            content_type__model='event',
            object_id=obj.id
        ).exists()

    def get_is_favorited(self, obj):
        """判断当前用户是否已收藏"""
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False

        return Favorite.objects.filter(
            user=request.user,
            content_type__model='event',
            object_id=obj.id
        ).exists()

    def get_display_status(self, obj):
        """展示用动态状态"""
        return obj.display_status

    def get_registration_count(self, obj):
        count = getattr(obj, 'approved_registration_count', None)
        if count is not None:
            return count
        return obj.registrations.filter(status='approved').count()


class EventAssignmentSerializer(serializers.ModelSerializer):
    """裁判任务序列化器"""
    event_title = serializers.CharField(source='event.title', read_only=True)
    event_start_time = serializers.DateTimeField(source='event.start_time', read_only=True)
    event_round = serializers.CharField(source='event.event_type', read_only=True)
    referee_name = serializers.CharField(source='referee.real_name', read_only=True)
    referee_username = serializers.CharField(source='referee.username', read_only=True)
    round_display = serializers.CharField(source='get_round_type_display', read_only=True)
    assigned_by_name = serializers.CharField(source='assigned_by.real_name', read_only=True)

    class Meta:
        model = EventAssignment
        fields = [
            'id', 'event', 'event_title', 'event_start_time', 'event_round',
            'referee', 'referee_name', 'referee_username', 'round_type',
            'round_display', 'assigned_by', 'assigned_by_name', 'remarks',
            'assigned_at'
        ]
        read_only_fields = ['id', 'assigned_by', 'assigned_at', 'event_title', 'referee_name', 'round_display', 'assigned_by_name']

    def create(self, validated_data):
        validated_data['assigned_by'] = self.context['request'].user
        return super().create(validated_data)


class RefereeEventAccessSerializer(serializers.ModelSerializer):
    """裁判赛事访问序列化器"""
    referee_name = serializers.CharField(source='referee.real_name', read_only=True)
    referee_username = serializers.CharField(source='referee.username', read_only=True)
    event_title = serializers.CharField(source='event.title', read_only=True)

    class Meta:
        model = RefereeEventAccess
        fields = ['id', 'referee', 'referee_name', 'referee_username', 'event', 'event_title']
        read_only_fields = ['id', 'referee_name', 'referee_username', 'event_title']
