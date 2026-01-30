"""
报名应用序列化器
"""
from rest_framework import serializers
from django.utils import timezone
from .models import Registration
import uuid


class RegistrationSerializer(serializers.ModelSerializer):
    """报名序列化器"""
    event_title = serializers.CharField(source='event.title', read_only=True)
    user_name = serializers.CharField(source='user.real_name', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    reviewed_by_name = serializers.CharField(source='reviewed_by.real_name', read_only=True)

    class Meta:
        model = Registration
        fields = [
            'id', 'event', 'event_title', 'user', 'user_name', 'user_username',
            'status', 'registration_number', 'participant_name', 'participant_phone',
            'participant_id_card', 'participant_gender', 'participant_birth_date',
            'participant_organization', 'emergency_contact', 'emergency_phone',
            'payment_status', 'payment_amount', 'payment_time', 'remarks',
            'review_remarks', 'reviewed_by', 'reviewed_by_name', 'reviewed_at',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'user', 'registration_number', 'reviewed_by', 'reviewed_at',
            'created_at', 'updated_at', 'event_title', 'user_name',
            'user_username', 'reviewed_by_name'
        ]

    def validate(self, attrs):
        """验证报名信息"""
        event = attrs.get('event')

        # 验证赛事状态
        if event.status not in ['published', 'ongoing']:
            raise serializers.ValidationError("该赛事不接受报名")

        # 验证报名时间
        now = timezone.now()
        if now < event.registration_start:
            raise serializers.ValidationError("报名尚未开始")
        if now > event.registration_end:
            raise serializers.ValidationError("报名已截止")

        # 验证人数限制
        if event.max_participants > 0 and event.current_participants >= event.max_participants:
            raise serializers.ValidationError("报名人数已满")

        return attrs

    def create(self, validated_data):
        """创建报名记录"""
        # 自动设置用户
        validated_data['user'] = self.context['request'].user

        # 生成报名编号
        event = validated_data['event']
        timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
        random_str = str(uuid.uuid4())[:8].upper()
        validated_data['registration_number'] = f"REG-{event.id}-{timestamp}-{random_str}"

        # 设置支付金额
        validated_data['payment_amount'] = event.registration_fee

        # 创建报名
        registration = super().create(validated_data)

        # 增加赛事的报名人数
        event.current_participants += 1
        event.save(update_fields=['current_participants'])

        return registration


class RegistrationCreateSerializer(serializers.ModelSerializer):
    """报名创建序列化器（简化版）"""

    class Meta:
        model = Registration
        fields = [
            'event', 'participant_name', 'participant_phone', 'participant_id_card',
            'participant_gender', 'participant_birth_date', 'participant_organization',
            'emergency_contact', 'emergency_phone', 'remarks'
        ]

    def validate(self, attrs):
        """验证报名信息"""
        event = attrs.get('event')
        user = self.context['request'].user

        # 检查是否已经报名
        if Registration.objects.filter(event=event, user=user).exists():
            raise serializers.ValidationError("您已经报名该赛事")

        # 验证赛事状态
        if event.status not in ['published', 'ongoing']:
            raise serializers.ValidationError("该赛事不接受报名")

        # 验证报名时间
        now = timezone.now()
        if now < event.registration_start:
            raise serializers.ValidationError("报名尚未开始")
        if now > event.registration_end:
            raise serializers.ValidationError("报名已截止")

        # 验证人数限制
        if event.max_participants > 0 and event.current_participants >= event.max_participants:
            raise serializers.ValidationError("报名人数已满")

        return attrs

    def create(self, validated_data):
        """创建报名记录"""
        # 自动设置用户
        validated_data['user'] = self.context['request'].user

        # 生成报名编号
        event = validated_data['event']
        timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
        random_str = str(uuid.uuid4())[:8].upper()
        validated_data['registration_number'] = f"REG-{event.id}-{timestamp}-{random_str}"

        # 设置支付金额
        validated_data['payment_amount'] = event.registration_fee

        # 创建报名
        registration = super().create(validated_data)

        # 增加赛事的报名人数
        event.current_participants += 1
        event.save(update_fields=['current_participants'])

        return registration


class RegistrationReviewSerializer(serializers.Serializer):
    """报名审核序列化器"""
    review_remarks = serializers.CharField(required=False, allow_blank=True)
