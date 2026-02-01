"""
报名应用视图
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.utils import timezone

from .models import Registration
from .serializers import (
    RegistrationSerializer,
    RegistrationCreateSerializer,
    RegistrationReviewSerializer
)
from utils.permissions import IsAdmin, IsAdminOrReferee, IsOwnerOrAdmin
from utils.export import export_registrations
from apps.events.models import Event


class RegistrationViewSet(viewsets.ModelViewSet):
    """
    报名视图集
    提供报名的CRUD操作
    """
    queryset = Registration.objects.select_related('event', 'user', 'reviewed_by').all()
    serializer_class = RegistrationSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'payment_status', 'event', 'user']
    search_fields = [
        'registration_number', 'participant_name', 'participant_phone',
        'participant_id_card', 'event__title', 'user__username'
    ]
    ordering_fields = ['created_at', 'status']
    ordering = ['-created_at']

    def get_permissions(self):
        """设置权限"""
        if self.action == 'create':
            # 创建报名需要认证
            permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            # 更新和删除需要是所有者或管理员
            permission_classes = [IsOwnerOrAdmin]
        elif self.action in ['approve', 'reject', 'export']:
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
