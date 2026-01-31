"""
轮播图应用视图
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from django.utils import timezone
from django.db.models import Q

from .models import Carousel
from .serializers import CarouselSerializer, CarouselListSerializer
from utils.permissions import IsAdmin, IsOwnerOrAdmin


class CarouselViewSet(viewsets.ModelViewSet):
    """
    轮播图视图集
    提供轮播图的CRUD操作
    """
    queryset = Carousel.objects.select_related('creator', 'event').all()
    serializer_class = CarouselSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['position', 'is_active', 'event']
    ordering_fields = ['order', 'created_at', 'click_count']
    ordering = ['order', '-created_at']

    def get_permissions(self):
        """设置权限"""
        if self.action in ['list', 'retrieve', 'active', 'by_position']:
            # 列表、详情、活动轮播图允许任何人访问
            permission_classes = [AllowAny]
        elif self.action == 'click':
            # 点击统计允许任何人访问
            permission_classes = [AllowAny]
        elif self.action == 'create':
            # 创建轮播图需要认证
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
            return CarouselListSerializer
        return CarouselSerializer

    def get_queryset(self):
        """普通用户只能看到已启用且在有效期内的轮播图"""
        user = self.request.user
        if user.is_authenticated and (user.is_superuser or user.user_type == 'admin'):
            return self.queryset

        now = timezone.now()
        return self.queryset.filter(
            is_active=True
        ).filter(
            Q(start_time__isnull=True) | Q(start_time__lte=now)
        ).filter(
            Q(end_time__isnull=True) | Q(end_time__gte=now)
        )

    @action(detail=False, methods=['get'])
    def active(self, request):
        """
        获取所有活动的轮播图
        GET /api/carousels/active/
        """
        now = timezone.now()
        carousels = self.queryset.filter(
            is_active=True
        ).filter(
            Q(start_time__isnull=True) | Q(start_time__lte=now)
        ).filter(
            Q(end_time__isnull=True) | Q(end_time__gte=now)
        ).order_by('order')

        serializer = CarouselListSerializer(carousels, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_position(self, request):
        """
        根据位置获取轮播图
        GET /api/carousels/by_position/?position=home
        """
        position = request.query_params.get('position', 'home')
        now = timezone.now()

        carousels = self.queryset.filter(
            is_active=True,
            position=position
        ).filter(
            Q(start_time__isnull=True) | Q(start_time__lte=now)
        ).filter(
            Q(end_time__isnull=True) | Q(end_time__gte=now)
        ).order_by('order')

        serializer = CarouselListSerializer(carousels, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def click(self, request, pk=None):
        """
        点击统计
        POST /api/carousels/{id}/click/
        """
        carousel = self.get_object()
        carousel.click_count += 1
        carousel.save(update_fields=['click_count'])

        return Response({
            'message': '点击统计已更新',
            'click_count': carousel.click_count
        })

    @action(detail=True, methods=['put'])
    def activate(self, request, pk=None):
        """
        启用轮播图
        PUT /api/carousels/{id}/activate/
        """
        carousel = self.get_object()
        carousel.is_active = True
        carousel.save()

        return Response({
            'message': '轮播图已启用',
            'carousel': CarouselSerializer(carousel).data
        })

    @action(detail=True, methods=['put'])
    def deactivate(self, request, pk=None):
        """
        禁用轮播图
        PUT /api/carousels/{id}/deactivate/
        """
        carousel = self.get_object()
        carousel.is_active = False
        carousel.save()

        return Response({
            'message': '轮播图已禁用',
            'carousel': CarouselSerializer(carousel).data
        })

    @action(detail=False, methods=['post'])
    def upload_image(self, request):
        """
        上传轮播图图片到前端public目录
        POST /api/carousels/upload_image/
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

        # 验证文件大小（5MB）
        if image_file.size > 5 * 1024 * 1024:
            return Response({
                'error': '图片大小不能超过 5MB'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 生成唯一文件名
        import uuid
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        random_str = str(uuid.uuid4())[:8]
        extension = image_file.name.split('.')[-1]
        filename = f'carousel_{timestamp}_{random_str}.{extension}'

        # 前端 public 目录路径
        frontend_public_dir = os.path.join(settings.BASE_DIR, '..', 'frontend', 'public', 'images', 'carousel')
        os.makedirs(frontend_public_dir, exist_ok=True)

        # 保存文件
        file_path = os.path.join(frontend_public_dir, filename)
        with open(file_path, 'wb+') as destination:
            for chunk in image_file.chunks():
                destination.write(chunk)

        # 返回相对路径
        relative_path = f'/images/carousel/{filename}'

        return Response({
            'message': '图片上传成功',
            'image': relative_path
        })
