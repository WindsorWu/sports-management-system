"""
反馈应用视图

提供反馈管理的REST API接口，支持用户反馈和管理员处理
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.utils import timezone

from .models import Feedback
from .serializers import (
    FeedbackSerializer,
    FeedbackCreateSerializer,
    FeedbackListSerializer,
    FeedbackReplySerializer
)
from utils.permissions import IsAdmin, IsOwnerOrAdmin


class FeedbackViewSet(viewsets.ModelViewSet):
    """
    反馈视图集
    
    提供反馈管理的CRUD操作和扩展功能
    
    主要功能:
        - 反馈提交: 用户提交各类反馈
        - 反馈查询: 查看反馈记录
        - 反馈回复: 管理员回复处理
        - 状态更新: 跟踪处理进度
        - 统计信息: 反馈统计数据
        - 匿名支持: 匿名反馈保护
        
    权限控制:
        - 创建: 需要登录认证
        - 列表/详情: 管理员看所有，用户只看自己的
        - 更新/删除: 需要是反馈所有者或管理员
        - 回复/状态更新: 需要管理员权限
        
    使用场景:
        - 用户报告问题
        - 用户提出建议
        - 用户投诉或表扬
        - 管理员处理反馈
    """
    queryset = Feedback.objects.select_related('user', 'event', 'handler').all()
    serializer_class = FeedbackSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['feedback_type', 'status', 'event', 'is_anonymous']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'status']
    ordering = ['-created_at']

    def get_permissions(self):
        """设置权限"""
        if self.action == 'create':
            # 创建反馈需要认证
            permission_classes = [IsAuthenticated]
        elif self.action in ['list', 'retrieve']:
            # 管理员可以查看所有反馈，普通用户只能查看自己的
            permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            # 更新和删除需要是所有者或管理员
            permission_classes = [IsOwnerOrAdmin]
        elif self.action in ['reply', 'update_status']:
            # 回复和更新状态需要管理员权限
            permission_classes = [IsAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        """根据不同操作返回不同的序列化器"""
        if self.action == 'create':
            return FeedbackCreateSerializer
        elif self.action == 'list':
            return FeedbackListSerializer
        elif self.action == 'reply':
            return FeedbackReplySerializer
        return FeedbackSerializer

    def get_queryset(self):
        """限制普通用户只能看到自己的反馈"""
        user = self.request.user
        if user.is_superuser or user.user_type == 'admin':
            return self.queryset
        return self.queryset.filter(user=user)

    def create(self, request, *args, **kwargs):
        """创建反馈"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        feedback = serializer.save()

        return Response({
            'message': '反馈提交成功',
            'feedback': FeedbackSerializer(feedback).data
        }, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def reply(self, request, pk=None):
        """
        回复反馈
        POST /api/feedbacks/{id}/reply/
        """
        feedback = self.get_object()

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        feedback.reply = serializer.validated_data['reply']
        feedback.status = serializer.validated_data.get('status', 'resolved')
        feedback.handler = request.user
        feedback.handled_at = timezone.now()
        feedback.save()

        return Response({
            'message': '回复成功',
            'feedback': FeedbackSerializer(feedback).data
        })

    @action(detail=True, methods=['put'])
    def update_status(self, request, pk=None):
        """
        更新反馈状态
        PUT /api/feedbacks/{id}/update_status/
        Body: {status: 'processing' | 'resolved' | 'closed'}
        """
        feedback = self.get_object()
        new_status = request.data.get('status')

        if not new_status or new_status not in dict(Feedback.STATUS_CHOICES):
            return Response({
                'error': '无效的状态值'
            }, status=status.HTTP_400_BAD_REQUEST)

        feedback.status = new_status
        if new_status in ['resolved', 'closed'] and not feedback.handled_at:
            feedback.handler = request.user
            feedback.handled_at = timezone.now()
        feedback.save()

        return Response({
            'message': '状态更新成功',
            'feedback': FeedbackSerializer(feedback).data
        })

    @action(detail=False, methods=['get'])
    def my_feedbacks(self, request):
        """
        获取当前用户的反馈
        GET /api/feedbacks/my_feedbacks/
        """
        feedbacks = self.queryset.filter(user=request.user)
        serializer = FeedbackSerializer(feedbacks, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def pending(self, request):
        """
        获取待处理的反馈（仅管理员）
        GET /api/feedbacks/pending/
        """
        feedbacks = self.queryset.filter(status='pending')
        serializer = FeedbackListSerializer(feedbacks, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """
        获取反馈统计（仅管理员）
        GET /api/feedbacks/statistics/
        """
        total = self.queryset.count()
        pending = self.queryset.filter(status='pending').count()
        processing = self.queryset.filter(status='processing').count()
        resolved = self.queryset.filter(status='resolved').count()
        closed = self.queryset.filter(status='closed').count()

        return Response({
            'total': total,
            'pending': pending,
            'processing': processing,
            'resolved': resolved,
            'closed': closed,
        })
