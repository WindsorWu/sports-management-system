"""
赛事应用序列化器
"""
from rest_framework import serializers
from .models import Event, EventAssignment, RefereeEventAccess
from apps.interactions.models import Favorite


class EventSerializer(serializers.ModelSerializer):
    """
    赛事基础序列化器
    
    用于赛事数据的序列化和反序列化，适用于创建、更新等操作
    包含赛事的完整信息字段
    
    额外字段:
        - organizer_name: 组织者真实姓名（只读）
        - organizer_username: 组织者用户名（只读）
    
    只读字段:
        - id: 赛事ID，系统自动生成
        - organizer: 组织者，创建时自动设置为当前用户
        - current_participants: 当前报名人数，根据报名记录计算
        - view_count: 浏览次数，通过点击接口增加
        - created_at, updated_at: 创建和更新时间
        - organizer_name, organizer_username: 组织者信息
    """
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
        """
        创建赛事时自动设置组织者为当前登录用户
        
        参数:
            validated_data: 经过验证的赛事数据
            
        返回:
            Event: 新创建的赛事对象
        """
        validated_data['organizer'] = self.context['request'].user
        return super().create(validated_data)


class EventListSerializer(serializers.ModelSerializer):
    """
    赛事列表序列化器（简化版）
    
    专门用于赛事列表展示，包含简化的字段和用户交互状态
    相比基础序列化器，增加了：
        - 用户交互状态（是否已报名、点赞、收藏）
        - 动态状态字段（根据时间自动判断赛事状态）
        - 字段别名（兼容前端不同的命名习惯）
    
    SerializerMethodField字段说明:
        - is_registered: 当前用户是否已报名
        - is_liked: 当前用户是否已点赞
        - is_favorited: 当前用户是否已收藏
        - display_status: 动态展示状态（根据时间自动判断）
        - registration_count: 已审核通过的报名人数
        
    字段别名（为兼容前端）:
        - name -> title
        - image -> cover_image
        - event_time -> start_time
        - registration_start_time -> registration_start
        - registration_end_time -> registration_end
        - click_count -> view_count
    """
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
        """
        判断当前用户是否已报名该赛事
        
        检查当前用户是否有pending或approved状态的报名记录
        
        返回:
            bool: 已报名返回True，否则返回False
        """
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False

        from apps.registrations.models import Registration
        return Registration.objects.filter(
            event=obj,
            user=request.user,
            status__in=['pending', 'approved']  # 只统计待审核和已通过的报名
        ).exists()

    def get_is_liked(self, obj):
        """
        判断当前用户是否已点赞该赛事
        
        通过查询Like表判断用户是否对该赛事点过赞
        
        返回:
            bool: 已点赞返回True，否则返回False
        """
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
        """
        判断当前用户是否已收藏该赛事
        
        通过查询Favorite表判断用户是否收藏了该赛事
        
        返回:
            bool: 已收藏返回True，否则返回False
        """
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False

        return Favorite.objects.filter(
            user=request.user,
            content_type__model='event',
            object_id=obj.id
        ).exists()

    def get_display_status(self, obj):
        """
        获取动态展示状态
        
        调用模型的display_status属性，根据当前时间
        自动判断赛事的实际状态（如已结束）
        
        返回:
            str: 赛事状态字符串
        """
        return obj.display_status

    def get_registration_count(self, obj):
        """
        获取已审核通过的报名人数
        
        优先使用查询集中预加载的计数（annotate），
        如果没有则查询数据库统计approved状态的报名数
        
        返回:
            int: 已通过审核的报名人数
        """
        count = getattr(obj, 'approved_registration_count', None)
        if count is not None:
            return count
        return obj.registrations.filter(status='approved').count()


class EventDetailSerializer(serializers.ModelSerializer):
    """
    赛事详情序列化器（完整版）
    
    用于展示单个赛事的完整详细信息
    相比列表序列化器，增加了更多的详细信息和业务逻辑判断
    
    额外字段说明:
        - organizer_info: 组织者的完整信息（ID、用户名、真实姓名、所属组织）
        - registration_count: 已通过审核的报名人数
        - can_register: 当前是否可以报名（综合时间、状态、人数限制判断）
        - is_registered: 当前用户是否已报名
        - is_liked: 当前用户是否已点赞
        - is_favorited: 当前用户是否已收藏
        - display_status: 动态展示状态
    
    can_register判断逻辑:
        1. 当前时间在报名时间范围内
        2. 赛事状态为published或ongoing
        3. 未达到最大参赛人数限制（0表示不限制）
    """
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
        """
        获取组织者的完整信息
        
        返回:
            dict: 包含组织者ID、用户名、真实姓名、所属组织
        """
        return {
            'id': obj.organizer.id,
            'username': obj.organizer.username,
            'real_name': obj.organizer.real_name,
            'organization': obj.organizer.organization,
        }

    def get_can_register(self, obj):
        """
        判断当前赛事是否可以报名
        
        综合考虑以下因素:
            1. 报名时间：当前时间必须在报名开始和结束时间之间
            2. 赛事状态：必须是已发布或进行中状态
            3. 人数限制：未达到最大参赛人数（0表示无限制）
        
        返回:
            bool: 可以报名返回True，否则返回False
        """
        from django.utils import timezone
        now = timezone.now()

        # 检查报名时间
        if now < obj.registration_start or now > obj.registration_end:
            return False

        # 检查赛事状态
        if obj.status not in ['published', 'ongoing']:
            return False

        # 检查人数限制（0表示不限制）
        if obj.max_participants > 0 and obj.current_participants >= obj.max_participants:
            return False

        return True

    def get_is_registered(self, obj):
        """
        判断当前用户是否已报名
        
        返回:
            bool: 已报名返回True，否则返回False
        """
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
        """
        判断当前用户是否已点赞
        
        返回:
            bool: 已点赞返回True，否则返回False
        """
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
        """
        判断当前用户是否已收藏
        
        返回:
            bool: 已收藏返回True，否则返回False
        """
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False

        return Favorite.objects.filter(
            user=request.user,
            content_type__model='event',
            object_id=obj.id
        ).exists()

    def get_display_status(self, obj):
        """
        获取动态展示状态
        
        返回:
            str: 赛事状态字符串
        """
        return obj.display_status

    def get_registration_count(self, obj):
        """
        获取已审核通过的报名人数
        
        返回:
            int: 已通过审核的报名人数
        """
        count = getattr(obj, 'approved_registration_count', None)
        if count is not None:
            return count
        return obj.registrations.filter(status='approved').count()


class EventAssignmentSerializer(serializers.ModelSerializer):
    """
    裁判任务序列化器
    
    用于管理裁判员的赛事任务分配
    将裁判分配到特定的赛事和比赛轮次
    
    额外只读字段:
        - event_title: 赛事标题
        - event_start_time: 赛事开始时间
        - event_round: 赛事类型
        - referee_name: 裁判真实姓名
        - referee_username: 裁判用户名
        - round_display: 轮次的可读名称（预赛、半决赛等）
        - assigned_by_name: 分配人姓名
    
    只读字段:
        - id: 任务ID
        - assigned_by: 分配人，创建时自动设置为当前用户
        - assigned_at: 分配时间
        - 以及所有额外的only_read字段
    """
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
        """
        创建任务时自动设置分配人为当前用户
        
        参数:
            validated_data: 经过验证的任务数据
            
        返回:
            EventAssignment: 新创建的任务对象
        """
        validated_data['assigned_by'] = self.context['request'].user
        return super().create(validated_data)


class RefereeEventAccessSerializer(serializers.ModelSerializer):
    """
    裁判赛事访问权限序列化器
    
    用于管理裁判员对特定赛事的访问权限
    控制裁判员可以查看和管理哪些赛事的成绩和报名信息
    
    额外只读字段:
        - referee_name: 裁判真实姓名
        - referee_username: 裁判用户名
        - event_title: 赛事标题
    
    只读字段:
        - id: 权限记录ID
        - referee_name, referee_username: 裁判信息
        - event_title: 赛事标题
        
    使用场景:
        - 管理员为裁判分配赛事访问权限
        - 查询裁判可访问的赛事列表
        - 查询赛事的裁判团队
    """
    referee_name = serializers.CharField(source='referee.real_name', read_only=True)
    referee_username = serializers.CharField(source='referee.username', read_only=True)
    event_title = serializers.CharField(source='event.title', read_only=True)

    class Meta:
        model = RefereeEventAccess
        fields = ['id', 'referee', 'referee_name', 'referee_username', 'event', 'event_title']
        read_only_fields = ['id', 'referee_name', 'referee_username', 'event_title']
