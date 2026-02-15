"""
成绩应用序列化器

提供成绩数据的序列化和反序列化功能，支持成绩录入、查询等业务逻辑
"""
from rest_framework import serializers
from .models import Result


class ResultSerializer(serializers.ModelSerializer):
    """
    成绩序列化器
    
    用于成绩数据的完整序列化，包含所有字段和关联信息
    
    主要功能:
        - 序列化成绩完整信息
        - 包含赛事、用户、报名、录入人等关联信息
        - 支持成绩创建时的自动字段填充
        - 验证成绩业务规则
        
    扩展字段说明:
        - event_title: 关联赛事的标题
        - user_name: 参赛运动员的真实姓名
        - user_username: 参赛运动员的用户名
        - recorded_by_name: 录入人的真实姓名
        - registration_number: 报名编号
        
    使用场景:
        - 成绩列表展示
        - 成绩详情查询
        - 排行榜显示
    """
    event_title = serializers.CharField(source='event.title', read_only=True)
    user_name = serializers.CharField(source='user.real_name', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    recorded_by_name = serializers.CharField(source='recorded_by.real_name', read_only=True)
    registration_number = serializers.CharField(source='registration.registration_number', read_only=True)

    class Meta:
        model = Result
        fields = [
            'id', 'event', 'event_title', 'registration', 'registration_number',
            'user', 'user_name', 'user_username', 'round_type', 'score',
            'rank', 'award', 'score_unit', 'remarks', 'certificate_url',
            'is_published', 'recorded_by', 'recorded_by_name',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'recorded_by', 'created_at', 'updated_at',
            'event_title', 'user_name', 'user_username', 'recorded_by_name',
            'registration_number'
        ]

    def validate(self, attrs):
        """
        验证成绩信息
        
        验证规则:
            1. 报名记录必须与赛事匹配
            2. 报名状态必须是已审核通过
            
        参数:
            attrs: 待验证的字段字典
            
        返回:
            验证通过的字段字典
            
        异常:
            ValidationError: 验证失败时抛出
        """
        registration = attrs.get('registration')
        event = attrs.get('event')

        # 验证报名记录和赛事是否匹配
        if registration and event and registration.event != event:
            raise serializers.ValidationError("报名记录与赛事不匹配")

        # 验证报名状态：只能为已审核通过的报名录入成绩
        if registration and registration.status != 'approved':
            raise serializers.ValidationError("该报名记录未通过审核")

        return attrs

    def create(self, validated_data):
        """
        创建成绩记录
        
        业务逻辑:
            1. 自动设置录入人为当前用户
            2. 自动从报名记录获取运动员信息
            
        参数:
            validated_data: 已验证的成绩数据
            
        返回:
            创建的成绩记录对象
        """
        # 自动设置录入人为当前用户
        validated_data['recorded_by'] = self.context['request'].user

        # 自动设置用户（从报名记录获取）
        if 'registration' in validated_data:
            validated_data['user'] = validated_data['registration'].user

        return super().create(validated_data)


class ResultCreateSerializer(serializers.ModelSerializer):
    """
    成绩创建序列化器（简化版）
    
    专门用于成绩录入的精简序列化器
    
    主要功能:
        - 只包含必要的成绩录入字段
        - 验证报名记录和赛事匹配
        - 防止同一轮次重复录入
        - 自动填充系统字段
        
    字段说明:
        - event: 赛事
        - registration: 报名记录
        - round_type: 比赛轮次
        - score: 成绩值
        - rank: 排名
        - award: 奖项
        - score_unit: 成绩单位
        - remarks: 备注
        - certificate_url: 证书链接
        - is_published: 是否公开
        
    使用场景:
        - 裁判录入成绩
        - Excel批量导入成绩
    """

    class Meta:
        model = Result
        fields = [
            'event', 'registration', 'round_type', 'score', 'rank',
            'award', 'score_unit', 'remarks', 'certificate_url', 'is_published'
        ]

    def validate(self, attrs):
        """
        验证成绩信息
        
        验证规则:
            1. 报名记录必须与赛事匹配
            2. 报名状态必须是已审核通过
            3. 同一选手在同一轮次不能重复录入成绩
        """
        registration = attrs.get('registration')
        event = attrs.get('event')

        # 验证报名记录和赛事是否匹配
        if registration.event != event:
            raise serializers.ValidationError("报名记录与赛事不匹配")

        # 验证报名状态：只能为已审核通过的报名录入成绩
        if registration.status != 'approved':
            raise serializers.ValidationError("该报名记录未通过审核")

        # 检查是否已经存在成绩：防止同一轮次重复录入
        if Result.objects.filter(
            event=event,
            registration=registration,
            round_type=attrs.get('round_type')
        ).exists():
            raise serializers.ValidationError("该选手在此轮次已有成绩记录")

        return attrs

    def create(self, validated_data):
        """
        创建成绩记录
        
        业务逻辑:
            1. 自动设置录入人为当前用户
            2. 自动从报名记录获取运动员信息
        """
        # 自动设置录入人为当前用户
        validated_data['recorded_by'] = self.context['request'].user

        # 自动设置用户（从报名记录获取）
        validated_data['user'] = validated_data['registration'].user

        return super().create(validated_data)


class ResultListSerializer(serializers.ModelSerializer):
    """
    成绩列表序列化器（简化版）
    
    用于成绩列表展示的精简序列化器
    
    主要功能:
        - 只包含列表展示必要的字段
        - 减少数据传输量
        - 提高列表查询性能
        
    使用场景:
        - 成绩列表页面
        - 排行榜显示
        - 移动端列表
    """
    event_title = serializers.CharField(source='event.title', read_only=True)
    user_name = serializers.CharField(source='user.real_name', read_only=True)

    class Meta:
        model = Result
        fields = [
            'id', 'event', 'event_title', 'user', 'user_name',
            'round_type', 'score', 'rank', 'award', 'score_unit',
            'is_published', 'created_at'
        ]

