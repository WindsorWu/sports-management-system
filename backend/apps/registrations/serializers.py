"""
报名应用序列化器

提供报名数据的序列化和反序列化功能，支持报名创建、审核等业务逻辑
"""
from rest_framework import serializers
from django.utils import timezone
from .models import Registration
import uuid


class RegistrationSerializer(serializers.ModelSerializer):
    """
    报名序列化器
    
    用于报名数据的完整序列化，包含所有字段和关联信息
    
    主要功能:
        - 序列化报名完整信息
        - 包含赛事标题、用户信息、审核人信息等关联数据
        - 支持报名创建时的自动字段填充
        - 验证报名业务规则
        
    扩展字段说明:
        - event_title: 关联赛事的标题
        - user_name: 报名用户的真实姓名
        - user_username: 报名用户的用户名
        - reviewed_by_name: 审核人的真实姓名
        
    使用场景:
        - 报名列表展示
        - 报名详情查询
        - 报名审核结果展示
    """
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
        """
        验证报名信息
        
        验证规则:
            1. 赛事状态必须是已发布或进行中
            2. 当前时间必须在报名时间范围内
            3. 未超出人数限制（如果设置了限制）
            
        参数:
            attrs: 待验证的字段字典
            
        返回:
            验证通过的字段字典
            
        异常:
            ValidationError: 验证失败时抛出，包含具体错误信息
        """
        event = attrs.get('event')

        # 验证赛事状态：只有已发布和进行中的赛事可以报名
        if event.status not in ['published', 'ongoing']:
            raise serializers.ValidationError("该赛事不接受报名")

        # 验证报名时间：必须在报名开始和结束时间之间
        now = timezone.now()
        if now < event.registration_start:
            raise serializers.ValidationError("报名尚未开始")
        if now > event.registration_end:
            raise serializers.ValidationError("报名已截止")

        # 验证人数限制：检查是否超出最大参赛人数（0表示不限制）
        if event.max_participants > 0 and event.current_participants >= event.max_participants:
            raise serializers.ValidationError("报名人数已满")

        return attrs

    def create(self, validated_data):
        """
        创建报名记录
        
        业务逻辑:
            1. 自动设置报名用户为当前登录用户
            2. 自动生成唯一的报名编号
            3. 从赛事获取报名费用
            4. 创建报名后增加赛事的当前报名人数
            
        报名编号格式:
            REG-{赛事ID}-{时间戳}-{随机字符串}
            例如: REG-123-20240101120000-A1B2C3D4
            
        参数:
            validated_data: 已验证的报名数据
            
        返回:
            创建的报名记录对象
        """
        # 自动设置用户为当前登录用户
        validated_data['user'] = self.context['request'].user

        # 生成唯一的报名编号
        event = validated_data['event']
        timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
        random_str = str(uuid.uuid4())[:8].upper()
        validated_data['registration_number'] = f"REG-{event.id}-{timestamp}-{random_str}"

        # 设置支付金额为赛事的报名费用
        validated_data['payment_amount'] = event.registration_fee

        # 创建报名记录
        registration = super().create(validated_data)

        # 增加赛事的当前报名人数
        event.current_participants += 1
        event.save(update_fields=['current_participants'])

        return registration


class RegistrationCreateSerializer(serializers.ModelSerializer):
    """
    报名创建序列化器（简化版）
    
    专门用于报名创建的精简序列化器，只包含用户填写的必要字段
    
    主要功能:
        - 只包含用户需要填写的报名字段
        - 自动检查用户是否重复报名
        - 完整的报名业务规则验证
        - 自动生成报名编号和系统字段
        
    字段说明:
        - event: 要报名的赛事
        - participant_*: 参赛者信息（姓名、电话、身份证等）
        - emergency_*: 紧急联系人信息
        - remarks: 备注信息
        
    使用场景:
        - 用户提交报名时使用
        - 前端报名表单数据提交
    """

    class Meta:
        model = Registration
        fields = [
            'event', 'participant_name', 'participant_phone', 'participant_id_card',
            'participant_gender', 'participant_birth_date', 'participant_organization',
            'emergency_contact', 'emergency_phone', 'remarks'
        ]

    def validate(self, attrs):
        """
        验证报名信息
        
        额外验证规则:
            1. 检查用户是否已经报名该赛事（防止重复报名）
            2. 验证赛事状态
            3. 验证报名时间
            4. 验证人数限制
            
        参数:
            attrs: 待验证的字段字典
            
        返回:
            验证通过的字段字典
            
        异常:
            ValidationError: 验证失败时抛出，包含具体错误信息
        """
        event = attrs.get('event')
        user = self.context['request'].user

        # 检查是否已经报名：同一用户不能重复报名同一赛事
        if Registration.objects.filter(event=event, user=user).exists():
            raise serializers.ValidationError("您已经报名该赛事")

        # 验证赛事状态：只有已发布和进行中的赛事可以报名
        if event.status not in ['published', 'ongoing']:
            raise serializers.ValidationError("该赛事不接受报名")

        # 验证报名时间：必须在报名开始和结束时间之间
        now = timezone.now()
        if now < event.registration_start:
            raise serializers.ValidationError("报名尚未开始")
        if now > event.registration_end:
            raise serializers.ValidationError("报名已截止")

        # 验证人数限制：检查是否超出最大参赛人数（0表示不限制）
        if event.max_participants > 0 and event.current_participants >= event.max_participants:
            raise serializers.ValidationError("报名人数已满")

        return attrs

    def create(self, validated_data):
        """
        创建报名记录
        
        业务逻辑:
            1. 自动设置报名用户为当前登录用户
            2. 自动生成唯一的报名编号
            3. 从赛事获取报名费用
            4. 创建报名后增加赛事的当前报名人数
            
        参数:
            validated_data: 已验证的报名数据
            
        返回:
            创建的报名记录对象
        """
        # 自动设置用户为当前登录用户
        validated_data['user'] = self.context['request'].user

        # 生成唯一的报名编号
        event = validated_data['event']
        timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
        random_str = str(uuid.uuid4())[:8].upper()
        validated_data['registration_number'] = f"REG-{event.id}-{timestamp}-{random_str}"

        # 设置支付金额为赛事的报名费用
        validated_data['payment_amount'] = event.registration_fee

        # 创建报名记录
        registration = super().create(validated_data)

        # 增加赛事的当前报名人数
        event.current_participants += 1
        event.save(update_fields=['current_participants'])

        return registration


class RegistrationReviewSerializer(serializers.Serializer):
    """
    报名审核序列化器
    
    用于单条报名审核时提交审核意见
    
    字段说明:
        - review_remarks: 审核备注，可以填写通过或拒绝的原因
        
    使用场景:
        - 管理员/裁判审核报名时使用
        - 支持通过和拒绝两种操作
    """
    review_remarks = serializers.CharField(
        required=False, 
        allow_blank=True,
        help_text='审核备注，说明通过或拒绝的原因'
    )


class RegistrationBulkReviewSerializer(serializers.Serializer):
    """
    批量审核序列化器
    
    用于批量审核多条报名记录
    
    字段说明:
        - ids: 要审核的报名ID列表，至少包含一个ID
        - review_remarks: 审核备注，所有报名使用相同的备注
        
    使用场景:
        - 管理员批量通过或拒绝报名
        - 提高审核效率
    """
    ids = serializers.ListField(
        child=serializers.IntegerField(), 
        min_length=1,
        help_text='要审核的报名ID列表'
    )
    review_remarks = serializers.CharField(
        required=False, 
        allow_blank=True,
        help_text='审核备注'
    )


class RegistrationBulkDeleteSerializer(serializers.Serializer):
    """
    批量删除序列化器
    
    用于批量删除多条报名记录
    
    字段说明:
        - ids: 要删除的报名ID列表，至少包含一个ID
        
    使用场景:
        - 管理员批量删除无效报名
        - 清理测试数据
        
    注意事项:
        - 删除操作不可恢复
        - 会同步更新赛事报名人数
    """
    ids = serializers.ListField(
        child=serializers.IntegerField(), 
        min_length=1,
        help_text='要删除的报名ID列表'
    )

