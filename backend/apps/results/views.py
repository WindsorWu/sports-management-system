"""
成绩应用视图
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Case, When, IntegerField
from rest_framework.exceptions import PermissionDenied

from .models import Result
from .serializers import ResultSerializer, ResultCreateSerializer, ResultListSerializer
from utils.permissions import IsAdmin, IsAdminOrReferee
from utils.export import export_results
from apps.events.models import RefereeEventAccess
from apps.registrations.models import Registration


class ResultViewSet(viewsets.ModelViewSet):
    """
    成绩视图集
    提供成绩的CRUD操作
    """
    queryset = Result.objects.select_related('event', 'user', 'registration', 'recorded_by').all()
    serializer_class = ResultSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['event', 'user', 'round_type', 'is_published']
    search_fields = [
        'user__username', 'user__real_name', 'event__title',
        'score', 'award'
    ]
    ordering_fields = ['created_at', 'rank', 'score']
    ordering = ['event', 'rank']

    def get_permissions(self):
        """设置权限"""
        if self.action in ['list', 'retrieve']:
            # 列表和详情允许任何人访问（但只能看到已公开的）
            permission_classes = [AllowAny]
        elif self.action in ['create', 'update', 'partial_update', 'destroy', 'publish', 'export', 'pending_results_count']:
            # 创建、更新、删除、公开、导出需要管理员或裁判权限
            permission_classes = [IsAdminOrReferee]
        else:
            # 其他操作需要认证
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        """根据不同操作返回不同的序列化器"""
        if self.action == 'create':
            return ResultCreateSerializer
        elif self.action == 'list':
            return ResultListSerializer
        return ResultSerializer

    def get_referee_event_ids(self, user):
        if not (user and user.is_authenticated and user.user_type == 'referee'):
            return None
        return list(RefereeEventAccess.objects.filter(referee=user).values_list('event_id', flat=True))

    def apply_referee_filter(self, queryset, user):
        referee_ids = self.get_referee_event_ids(user)
        if referee_ids is None:
            return queryset
        return queryset.filter(event_id__in=referee_ids)

    def get_queryset(self):
        """普通用户只能看到已公开的成绩"""
        user = self.request.user
        if user.is_authenticated and (user.is_superuser or user.user_type in ['admin', 'organizer']):
            return self.queryset
        base = self.queryset.filter(is_published=True)
        return self.apply_referee_filter(base, user)

    def create(self, request, *args, **kwargs):
        """创建成绩"""
        referee_events = self.get_referee_event_ids(request.user)
        event_id = request.data.get('event')
        if referee_events is not None and event_id and int(event_id) not in referee_events:
            raise PermissionDenied('该裁判未被分配该赛事')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.save()
        return Response({
            'message': '成绩录入成功',
            'result': ResultSerializer(result).data
        }, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['put'])
    def publish(self, request, pk=None):
        """
        公开成绩
        PUT /api/results/{id}/publish/
        """
        result = self.get_object()
        result.is_published = True
        result.save()

        return Response({
            'message': '成绩已公开',
            'result': ResultSerializer(result).data
        })

    @action(detail=True, methods=['put'])
    def unpublish(self, request, pk=None):
        """
        取消公开成绩
        PUT /api/results/{id}/unpublish/
        """
        result = self.get_object()
        result.is_published = False
        result.save()

        return Response({
            'message': '成绩已取消公开',
            'result': ResultSerializer(result).data
        })

    @action(detail=False, methods=['get'])
    def export(self, request):
        """
        导出成绩表
        GET /api/results/export/?event={event_id}
        """
        # 获取查询参数
        event_id = request.query_params.get('event')
        round_type = request.query_params.get('round_type')

        queryset = Result.objects.select_related('event', 'user', 'registration').all()
        queryset = self.apply_referee_filter(queryset, request.user)

        if event_id:
            queryset = queryset.filter(event_id=event_id)
        if round_type:
            queryset = queryset.filter(round_type=round_type)

        round_order = Case(
            When(round_type='final', then=1),
            When(round_type='semifinal', then=2),
            When(round_type='preliminary', then=3),
            default=4,
            output_field=IntegerField()
        )
        queryset = queryset.order_by(round_order, 'rank', 'score')

        # 使用导出工具导出
        return export_results(queryset)

    @action(detail=False, methods=['get'])
    def leaderboard(self, request):
        """
        获取排行榜
        GET /api/results/leaderboard/?event={event_id}&round_type={round_type}
        """
        event_id = request.query_params.get('event')
        round_type = request.query_params.get('round_type', 'final')

        if not event_id:
            return Response({
                'error': '请提供赛事ID'
            }, status=status.HTTP_400_BAD_REQUEST)

        results = self.apply_referee_filter(self.queryset, request.user).filter(
            event_id=event_id,
            round_type=round_type,
            is_published=True
        ).order_by('rank')[:10]  # 只返回前10名

        serializer = ResultListSerializer(results, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def my_results(self, request):
        """
        获取当前用户的成绩
        GET /api/results/my_results/
        """
        if not request.user.is_authenticated:
            return Response({
                'error': '请先登录'
            }, status=status.HTTP_401_UNAUTHORIZED)

        base_results = Result.objects.filter(
            user=request.user,
            is_published=True
        ).select_related('event', 'registration')
        results = self.apply_referee_filter(base_results, request.user)

        serializer = ResultSerializer(results, many=True)
        return Response(serializer.data)

    def get_pending_results_count(self, event_ids=None):
        queryset = Result.objects.select_related('event', 'registration')
        recorded_ids = set(queryset.filter(event_id__in=event_ids).values_list('registration_id', flat=True)) if event_ids else set()
        reg_queryset = Registration.objects.filter(status='approved')
        if event_ids:
            reg_queryset = reg_queryset.filter(event_id__in=event_ids)
        if recorded_ids:
            reg_queryset = reg_queryset.exclude(id__in=recorded_ids)
        return reg_queryset.count()

    @action(detail=False, methods=['get'])
    def pending_results_count(self, request):
        """管理员/裁判：获取裁判负责赛事中未录入的运动员数"""
        user = request.user
        if user.is_authenticated and (user.is_superuser or user.user_type in ['admin', 'organizer']):
            count = self.get_pending_results_count()
            return Response({'count': count})

        event_ids = self.get_referee_event_ids(user)
        if not event_ids:
            return Response({'count': 0})
        count = self.get_pending_results_count(event_ids)
        return Response({'count': count})
