"""
报名应用视图

提供报名管理的完整REST API接口，包括报名提交、审核、导出等功能
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.utils import timezone
from django.db import transaction

from .models import Registration
from .serializers import (
    RegistrationSerializer,
    RegistrationCreateSerializer,
    RegistrationReviewSerializer,
    RegistrationBulkReviewSerializer,
    RegistrationBulkDeleteSerializer
)
from utils.permissions import IsAdmin, IsAdminOrReferee, IsOwnerOrAdmin
from utils.export import export_registrations
from apps.events.models import Event


class RegistrationViewSet(viewsets.ModelViewSet):
    """
    报名视图集
    
    提供报名管理的CRUD操作和扩展功能
    
    主要功能:
        - 报名提交: 用户提交报名信息，自动生成报名编号
        - 报名审核: 管理员/裁判审核报名，支持批量操作
        - 报名查询: 支持多条件筛选和搜索
        - 报名导出: 导出Excel格式的报名名单
        - 报名取消: 用户自主取消报名
        
    权限控制:
        - 创建: 需要登录认证
        - 查看: 普通用户只能看自己的报名，管理员可看全部
        - 审核: 需要管理员或裁判权限
        - 导出: 需要管理员或裁判权限
        
    使用场景:
        - 运动员报名参加赛事
        - 组织者审核报名申请
        - 导出报名名单用于赛事安排
    """
    queryset = Registration.objects.select_related('event', 'user', 'reviewed_by').all()
    serializer_class = RegistrationSerializer
    # 配置过滤、搜索、排序后端
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # 支持按以下字段精确筛选
    filterset_fields = ['status', 'payment_status', 'event', 'user']
    # 支持按以下字段模糊搜索
    search_fields = [
        'registration_number', 'participant_name', 'participant_phone',
        'participant_id_card', 'event__title', 'user__username'
    ]
    # 支持按以下字段排序
    ordering_fields = ['created_at', 'status']
    ordering = ['-created_at']  # 默认按报名时间倒序

    def get_permissions(self):
        """
        根据不同操作动态设置权限
        
        权限说明:
            - create: 创建报名需要登录认证
            - update/destroy: 更新和删除需要是报名所有者或管理员
            - 审核操作: 需要管理员或裁判权限
            - export: 导出需要管理员或裁判权限
            - 其他: 需要登录认证
        """
        if self.action == 'create':
            # 创建报名需要认证
            permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            # 更新和删除需要是所有者或管理员
            permission_classes = [IsOwnerOrAdmin]
        elif self.action in ['approve', 'reject', 'export', 'bulk_approve', 'bulk_reject', 'bulk_delete']:
            # 审核和导出需要管理员或裁判权限
            permission_classes = [IsAdminOrReferee]
        else:
            # 其他操作需要认证
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        """根据不同操作返回不同的序列化器"""
        if self.action == 'create':
            return RegistrationCreateSerializer
        elif self.action in ['approve', 'reject']:
            return RegistrationReviewSerializer
        return RegistrationSerializer

    def get_queryset(self):
        """限制普通用户只能看到自己的报名"""
        user = self.request.user
        if user.is_superuser or user.user_type in ['admin', 'organizer']:
            return self.queryset
        return self.queryset.filter(user=user)

    def create(self, request, *args, **kwargs):
        """创建报名"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        registration = serializer.save()
        return Response({
            'message': '报名成功',
            'registration': RegistrationSerializer(registration).data
        }, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['put'])
    def approve(self, request, pk=None):
        """
        审核通过
        PUT /api/registrations/{id}/approve/
        """
        registration = self.get_object()

        if registration.status != 'pending':
            return Response({
                'error': '该报名记录已审核'
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        registration.status = 'approved'
        registration.review_remarks = serializer.validated_data.get('review_remarks', '')
        registration.reviewed_by = request.user
        registration.reviewed_at = timezone.now()
        registration.save()

        return Response({
            'message': '审核通过',
            'registration': RegistrationSerializer(registration).data
        })

    @action(detail=True, methods=['put'])
    def reject(self, request, pk=None):
        """
        审核拒绝
        PUT /api/registrations/{id}/reject/
        """
        registration = self.get_object()

        if registration.status != 'pending':
            return Response({
                'error': '该报名记录已审核'
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        registration.status = 'rejected'
        registration.review_remarks = serializer.validated_data.get('review_remarks', '')
        registration.reviewed_by = request.user
        registration.reviewed_at = timezone.now()
        registration.save()

        # 减少赛事的报名人数
        event = registration.event
        if event.current_participants > 0:
            event.current_participants -= 1
            event.save(update_fields=['current_participants'])

        return Response({
            'message': '审核拒绝',
            'registration': RegistrationSerializer(registration).data
        })

    @action(detail=True, methods=['put'])
    def cancel(self, request, pk=None):
        """
        取消报名
        PUT /api/registrations/{id}/cancel/
        """
        registration = self.get_object()

        # 只有报名者本人可以取消
        if registration.user != request.user and not request.user.is_superuser:
            return Response({
                'error': '无权取消该报名'
            }, status=status.HTTP_403_FORBIDDEN)

        if registration.status == 'cancelled':
            return Response({
                'error': '报名已取消'
            }, status=status.HTTP_400_BAD_REQUEST)

        registration.status = 'cancelled'
        registration.save()

        # 减少赛事的报名人数
        event = registration.event
        if event.current_participants > 0:
            event.current_participants -= 1
            event.save(update_fields=['current_participants'])

        return Response({
            'message': '取消报名成功',
            'registration': RegistrationSerializer(registration).data
        })

    @action(detail=False, methods=['get'])
    def export(self, request):
        """
        导出报名名单
        GET /api/registrations/export/?event={event_id}
        """
        # 获取查询参数
        event_id = request.query_params.get('event')
        status_filter = request.query_params.get('status')

        if not event_id:
            return Response({
                'error': '请先选择一个赛事'
            }, status=status.HTTP_400_BAD_REQUEST)

        event = Event.objects.filter(id=event_id).first()
        if not event:
            return Response({
                'error': '赛事不存在'
            }, status=status.HTTP_400_BAD_REQUEST)

        queryset = self.get_queryset()

        if event_id:
            queryset = queryset.filter(event_id=event_id)
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        # 使用导出工具导出
        return export_registrations(queryset, event_title=event.title)

    @action(detail=False, methods=['get'])
    def my_registrations(self, request):
        """
        获取当前用户的报名记录
        GET /api/registrations/my_registrations/
        """
        registrations = self.queryset.filter(user=request.user)
        serializer = RegistrationSerializer(registrations, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def bulk_approve(self, request):
        """
        批量通过审核
        
        POST /api/registrations/bulk_approve/
        Body: {ids: [1, 2, 3], review_remarks: '审核通过'}
        
        功能说明:
            - 批量审核多条待审核报名记录
            - 只处理状态为pending的报名
            - 自动记录审核人和审核时间
            
        参数:
            - ids: 要审核的报名ID列表（必填）
            - review_remarks: 审核备注（可选）
            
        返回:
            - message: 操作结果消息
            - approved_ids: 成功审核通过的ID列表
        """
        serializer = RegistrationBulkReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        ids = serializer.validated_data['ids']
        review_remarks = serializer.validated_data.get('review_remarks', '')
        queryset = self.get_queryset().filter(id__in=ids, status='pending')
        if not queryset.exists():
            return Response({'error': '未找到任何待审核的报名'}, status=status.HTTP_400_BAD_REQUEST)

        now = timezone.now()
        approved_ids = []
        for registration in queryset:
            registration.status = 'approved'
            registration.review_remarks = review_remarks
            registration.reviewed_by = request.user
            registration.reviewed_at = now
            registration.save(update_fields=['status', 'review_remarks', 'reviewed_by', 'reviewed_at'])
            approved_ids.append(registration.id)

        return Response({
            'message': f'成功通过 {len(approved_ids)} 条报名',
            'approved_ids': approved_ids
        })

    @action(detail=False, methods=['post'])
    def bulk_reject(self, request):
        """
        批量驳回报名
        
        POST /api/registrations/bulk_reject/
        Body: {ids: [1, 2, 3], review_remarks: '不符合条件'}
        
        功能说明:
            - 批量驳回多条报名记录
            - 可处理pending和approved状态的报名
            - 驳回后会减少赛事的报名人数
            - 自动记录审核人和审核时间
            
        参数:
            - ids: 要驳回的报名ID列表（必填）
            - review_remarks: 驳回理由（可选）
            
        返回:
            - message: 操作结果消息
            - rejected_ids: 成功驳回的ID列表
        """
        serializer = RegistrationBulkReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        ids = serializer.validated_data['ids']
        review_remarks = serializer.validated_data.get('review_remarks', '')
        queryset = self.get_queryset().filter(id__in=ids, status__in=['pending', 'approved'])
        if not queryset.exists():
            return Response({'error': '未找到任何待审核的报名'}, status=status.HTTP_400_BAD_REQUEST)

        now = timezone.now()
        rejected_ids = []
        for registration in queryset:
            registration.status = 'rejected'
            registration.review_remarks = review_remarks
            registration.reviewed_by = request.user
            registration.reviewed_at = now
            registration.save(update_fields=['status', 'review_remarks', 'reviewed_by', 'reviewed_at'])

            event = registration.event
            if event.current_participants > 0:
                event.current_participants -= 1
                event.save(update_fields=['current_participants'])

            rejected_ids.append(registration.id)

        return Response({
            'message': f'成功驳回 {len(rejected_ids)} 条报名',
            'rejected_ids': rejected_ids
        })

    @action(detail=False, methods=['post'])
    def bulk_delete(self, request):
        """
        批量删除报名
        
        POST /api/registrations/bulk_delete/
        Body: {ids: [1, 2, 3]}
        
        功能说明:
            - 批量删除多条报名记录
            - 会同步更新赛事的报名人数
            - 使用数据库事务确保数据一致性
            - 只有未取消/未拒绝的报名才会减少人数
            
        参数:
            - ids: 要删除的报名ID列表（必填）
            
        返回:
            - message: 操作结果消息
            - deleted_ids: 成功删除的ID列表
            
        注意事项:
            - 删除操作不可恢复，请谨慎使用
            - 需要管理员或裁判权限
        """
        serializer = RegistrationBulkDeleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        ids = serializer.validated_data['ids']
        queryset = self.get_queryset().filter(id__in=ids)
        if not queryset.exists():
            return Response({'error': '没有找到任何要删除的报名'}, status=status.HTTP_400_BAD_REQUEST)

        deleted_ids = []
        with transaction.atomic():
            for registration in queryset.select_related('event'):
                event = registration.event
                # 仅对未被取消/拒绝的报名减少人数
                if registration.status in ['pending', 'approved'] and event.current_participants > 0:
                    event.current_participants -= 1
                    event.save(update_fields=['current_participants'])
                deleted_ids.append(registration.id)
            queryset.delete()

        return Response({
            'message': f'成功删除 {len(deleted_ids)} 条报名',
            'deleted_ids': deleted_ids
        })
