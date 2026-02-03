"""
成绩应用序列化器
"""
from rest_framework import serializers
from .models import Result


class ResultSerializer(serializers.ModelSerializer):
    """成绩序列化器"""
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
        """验证成绩信息"""
        registration = attrs.get('registration')
        event = attrs.get('event')

        # 验证报名记录和赛事是否匹配
        if registration and event and registration.event != event:
            raise serializers.ValidationError("报名记录与赛事不匹配")

        # 验证报名状态
        if registration and registration.status != 'approved':
            raise serializers.ValidationError("该报名记录未通过审核")

        return attrs

    def create(self, validated_data):
        """创建成绩记录"""
        # 自动设置录入人
        validated_data['recorded_by'] = self.context['request'].user

        # 自动设置用户（从报名记录获取）
        if 'registration' in validated_data:
            validated_data['user'] = validated_data['registration'].user

        return super().create(validated_data)


class ResultCreateSerializer(serializers.ModelSerializer):
    """成绩创建序列化器（简化版）"""

    class Meta:
        model = Result
        fields = [
            'event', 'registration', 'round_type', 'score', 'rank',
            'award', 'score_unit', 'remarks', 'certificate_url', 'is_published'
        ]

    def validate(self, attrs):
        """验证成绩信息"""
        registration = attrs.get('registration')
        event = attrs.get('event')

        # 验证报名记录和赛事是否匹配
        if registration.event != event:
            raise serializers.ValidationError("报名记录与赛事不匹配")

        # 验证报名状态
        if registration.status != 'approved':
            raise serializers.ValidationError("该报名记录未通过审核")

        # 检查是否已经存在成绩
        if Result.objects.filter(
            event=event,
            registration=registration,
            round_type=attrs.get('round_type')
        ).exists():
            raise serializers.ValidationError("该选手在此轮次已有成绩记录")

        return attrs

    def create(self, validated_data):
        """创建成绩记录"""
        # 自动设置录入人
        validated_data['recorded_by'] = self.context['request'].user

        # 自动设置用户（从报名记录获取）
        validated_data['user'] = validated_data['registration'].user

        return super().create(validated_data)


class ResultListSerializer(serializers.ModelSerializer):
    """成绩列表序列化器（简化版）"""
    event_title = serializers.CharField(source='event.title', read_only=True)
    user_name = serializers.CharField(source='user.real_name', read_only=True)

    class Meta:
        model = Result
        fields = [
            'id', 'event', 'event_title', 'user', 'user_name',
            'round_type', 'score', 'rank', 'award', 'score_unit',
            'is_published', 'created_at'
        ]

