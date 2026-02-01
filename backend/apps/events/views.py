"""
赛事应用视图
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.exceptions import PermissionDenied
from django.utils import timezone
from django.db.models import Q
from django.db import transaction
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Event, EventAssignment, RefereeEventAccess
from .serializers import EventSerializer, EventListSerializer, EventDetailSerializer, EventAssignmentSerializer, RefereeEventAccessSerializer
from utils.permissions import IsAdmin, IsOwnerOrAdmin, IsAuthenticatedOrReadOnly, IsAdminOrReferee, IsSuperAdminOrAdminRole
from utils.export import export_results


class EventViewSet(viewsets.ModelViewSet):
    """
    赛事视图集
    提供赛事的CRUD操作
    """
    queryset = Event.objects.select_related('organizer').all()
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['event_type', 'level', 'is_featured']
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
        elif self.action == 'registrations':
            # 报名列表需管理员或裁判
            permission_classes = [IsAdminOrReferee]
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

    @action(detail=False, methods=['post'])
    def upload_image(self, request):
        """
        上传赛事图片到前端public目录
        POST /api/events/upload_image/
        """
        import os
        from django.conf import settings

        # el-upload 默认使用 'file' 字段名
        if 'file' not in request.FILES and 'image' not in request.FILES:
            return Response({
                'error': '请上传图片文件'
            }, status=status.HTTP_400_BAD_REQUEST)

        image_file = request.FILES.get('file') or request.FILES.get('image')

        # 验证文件类型
        allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp']
        if image_file.content_type not in allowed_types:
            return Response({
                'error': '只支持 jpg, png, gif, webp 格式的图片'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 验证文件大小（2MB）
        if image_file.size > 2 * 1024 * 1024:
            return Response({
                'error': '图片大小不能超过 2MB'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 生成唯一文件名
        import uuid
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        random_str = str(uuid.uuid4())[:8]
        extension = image_file.name.split('.')[-1]
        filename = f'event_{timestamp}_{random_str}.{extension}'

        # 前端 public 目录路径
        frontend_public_dir = os.path.join(settings.BASE_DIR, '..', 'frontend', 'public', 'images', 'events')
        os.makedirs(frontend_public_dir, exist_ok=True)

        # 保存文件
        file_path = os.path.join(frontend_public_dir, filename)
        with open(file_path, 'wb+') as destination:
            for chunk in image_file.chunks():
                destination.write(chunk)

        # 返回相对路径
        relative_path = f'/images/events/{filename}'

        return Response({
            'message': '图片上传成功',
            'image': relative_path
        })

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

    def get_queryset(self):
        queryset = super().get_queryset()
        status_param = self.request.query_params.get('status')
        if not status_param:
            return queryset

        now = timezone.now()
        if status_param == 'finished':
            finished_filter = (
                Q(status='finished') |
                (Q(status__in=['published', 'ongoing']) & Q(end_time__lt=now))
            )
            return queryset.filter(finished_filter)

        return queryset.filter(status=status_param)


class EventAssignmentViewSet(viewsets.ModelViewSet):
    """赛事任务管理"""
    queryset = EventAssignment.objects.select_related('event', 'referee', 'assigned_by').all()
    serializer_class = EventAssignmentSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['event', 'referee', 'round_type']
    ordering_fields = ['assigned_at']
    ordering = ['-assigned_at']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminOrReferee]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.user_type == 'referee':
            return self.queryset.filter(referee=user)
        return self.queryset

    def ensure_admin(self):
        user = self.request.user
        if not user.is_authenticated or (not user.is_superuser and user.user_type != 'admin'):
            raise PermissionDenied('仅管理员可以修改赛事任务')

    def create(self, request, *args, **kwargs):
        self.ensure_admin()
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self.ensure_admin()
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        self.ensure_admin()
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        self.ensure_admin()
        return super().destroy(request, *args, **kwargs)


class RefereeEventAccessViewSet(viewsets.ModelViewSet):
    """裁判赛事管理"""
    queryset = RefereeEventAccess.objects.select_related('referee', 'event').all()
    serializer_class = RefereeEventAccessSerializer
    permission_classes = [IsSuperAdminOrAdminRole]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['referee']

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def assign(self, request):
        """为某个裁判更新可访问赛事"""
        referee_id = request.data.get('referee')
        event_ids = request.data.get('event_ids', [])
        if not referee_id:
            return Response({'error': '请提供裁判ID'}, status=status.HTTP_400_BAD_REQUEST)
        if not isinstance(event_ids, list):
            return Response({'error': 'event_ids 必须是数组'}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            RefereeEventAccess.objects.filter(referee_id=referee_id).exclude(event_id__in=event_ids).delete()
            existing_ids = set(RefereeEventAccess.objects.filter(referee_id=referee_id).values_list('event_id', flat=True))
            to_create = [RefereeEventAccess(referee_id=referee_id, event_id=event_id) for event_id in event_ids if event_id not in existing_ids]
            RefereeEventAccess.objects.bulk_create(to_create)

        queryset = RefereeEventAccess.objects.filter(referee_id=referee_id).select_related('event')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_events(self, request):
        """返回当前裁判可以访问的赛事"""
        user = request.user
        if not user.is_authenticated or user.user_type != 'referee':
            return Response([], status=status.HTTP_200_OK)

        accesses = RefereeEventAccess.objects.filter(referee=user).select_related('event')
        events = [access.event for access in accesses]
        serializer = EventListSerializer(events, many=True, context={'request': request})
        return Response(serializer.data)

