"""
赛事应用视图
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.utils import timezone
from django.db.models import Q

from .models import Event
from .serializers import EventSerializer, EventListSerializer, EventDetailSerializer
from utils.permissions import IsAdmin, IsOwnerOrAdmin, IsAuthenticatedOrReadOnly


class EventViewSet(viewsets.ModelViewSet):
    """
    赛事视图集
    提供赛事的CRUD操作
    """
    queryset = Event.objects.select_related('organizer').all()
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'event_type', 'level', 'is_featured']
    search_fields = ['title', 'description', 'location', 'event_type']
    ordering_fields = ['created_at', 'start_time', 'view_count']
    ordering = ['-created_at']

    def get_permissions(self):
        """设置权限"""
        if self.action in ['list', 'retrieve', 'featured', 'upcoming']:
            # 列表、详情、推荐、即将开始的赛事允许任何人访问
            permission_classes = [AllowAny]
        elif self.action == 'click':
            # 点击统计允许任何人访问
            permission_classes = [AllowAny]
        elif self.action == 'create':
            # 创建赛事需要认证
            permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            # 更新和删除需要是所有者或管理员
            permission_classes = [IsOwnerOrAdmin]
        else:
            # 其他操作需要管理员权限
            permission_classes = [IsAdmin]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        """根据不同操作返回不同的序列化器"""
        if self.action == 'list':
            return EventListSerializer
        elif self.action == 'retrieve':
            return EventDetailSerializer
        return EventSerializer

    def retrieve(self, request, *args, **kwargs):
        """获取赛事详情（不增加浏览次数）"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def click(self, request, pk=None):
        """
        点击统计（增加浏览次数）
        POST /api/events/{id}/click/
        """
        event = self.get_object()
        event.view_count += 1
        event.save(update_fields=['view_count'])
        return Response({
            'message': '浏览次数已更新',
            'view_count': event.view_count
        })

    @action(detail=False, methods=['get'])
    def featured(self, request):
        """
        获取推荐赛事
        GET /api/events/featured/
        """
        events = self.queryset.filter(is_featured=True, status='published')
        serializer = EventListSerializer(events, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """
        获取即将开始的赛事
        GET /api/events/upcoming/
        """
        now = timezone.now()
        events = self.queryset.filter(
            status='published',
            start_time__gte=now
        ).order_by('start_time')[:10]
        serializer = EventListSerializer(events, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def ongoing(self, request):
        """
        获取正在进行的赛事
        GET /api/events/ongoing/
        """
        now = timezone.now()
        events = self.queryset.filter(
            Q(status='ongoing') |
            Q(status='published', start_time__lte=now, end_time__gte=now)
        )
        serializer = EventListSerializer(events, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def can_register(self, request):
        """
        获取可以报名的赛事
        GET /api/events/can_register/
        """
        now = timezone.now()
        events = self.queryset.filter(
            status__in=['published', 'ongoing'],
            registration_start__lte=now,
            registration_end__gte=now
        )
        serializer = EventListSerializer(events, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def registrations(self, request, pk=None):
        """
        获取赛事的报名记录
        GET /api/events/{id}/registrations/
        """
        event = self.get_object()
        registrations = event.registrations.select_related('user').all()

        from apps.registrations.serializers import RegistrationSerializer
        serializer = RegistrationSerializer(registrations, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def results(self, request, pk=None):
        """
        获取赛事的成绩列表
        GET /api/events/{id}/results/
        """
        event = self.get_object()
        results = event.results.select_related('user', 'registration').filter(
            is_published=True
        ).order_by('rank')

        from apps.results.serializers import ResultSerializer
        serializer = ResultSerializer(results, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def announcements(self, request, pk=None):
        """
        获取赛事相关的公告
        GET /api/events/{id}/announcements/
        """
        event = self.get_object()
        announcements = event.announcements.filter(is_published=True).order_by('-is_pinned', '-publish_time')

        from apps.announcements.serializers import AnnouncementSerializer
        serializer = AnnouncementSerializer(announcements, many=True)
        return Response(serializer.data)
