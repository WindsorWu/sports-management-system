"""
成绩应用视图
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Result
from .serializers import ResultSerializer, ResultCreateSerializer, ResultListSerializer
from utils.permissions import IsAdmin, IsAdminOrReferee
from utils.export import export_results


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
        elif self.action in ['create', 'update', 'partial_update', 'destroy', 'publish', 'export']:
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

    def get_queryset(self):
        """普通用户只能看到已公开的成绩"""
        user = self.request.user
        if user.is_authenticated and (user.is_superuser or user.user_type in ['admin', 'organizer']):
            return self.queryset
        return self.queryset.filter(is_published=True)

    def create(self, request, *args, **kwargs):
        """创建成绩"""
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

        if event_id:
            queryset = queryset.filter(event_id=event_id)
        if round_type:
            queryset = queryset.filter(round_type=round_type)

        # 按排名排序
        queryset = queryset.order_by('event', 'rank')

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

        results = self.queryset.filter(
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

        results = Result.objects.filter(
            user=request.user,
            is_published=True
        ).select_related('event', 'registration')

        serializer = ResultSerializer(results, many=True)
        return Response(serializer.data)
