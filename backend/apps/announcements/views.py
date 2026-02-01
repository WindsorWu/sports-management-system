"""
公告应用视图
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.utils import timezone
import os
import uuid
from datetime import datetime
from django.conf import settings

from .models import Announcement
from .serializers import (
    AnnouncementSerializer,
    AnnouncementListSerializer,
    AnnouncementDetailSerializer
)
from utils.permissions import IsAdmin, IsOwnerOrAdmin


class AnnouncementViewSet(viewsets.ModelViewSet):
    """
    公告视图集
    提供公告的CRUD操作
    """
    queryset = Announcement.objects.select_related('author', 'event').all()
    serializer_class = AnnouncementSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['announcement_type', 'priority', 'is_published', 'is_pinned', 'event']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'publish_time', 'priority', 'is_pinned']
    ordering = ['-is_pinned', '-publish_time', '-created_at']

    def get_permissions(self):
        """设置权限"""
        if self.action in ['list', 'retrieve', 'published', 'pinned']:
            # 列表、详情、已发布、置顶公告允许任何人访问
            permission_classes = [AllowAny]
        elif self.action == 'create':
            # 创建公告需要认证
            permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            # 更新和删除需要是所有者或管理员
            permission_classes = [IsOwnerOrAdmin]
        elif self.action == 'upload_image':
            # 上传图片需要管理员权限
            permission_classes = [IsAdmin]
        else:
            # 其他操作需要管理员权限
            permission_classes = [IsAdmin]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        """根据不同操作返回不同的序列化器"""
        if self.action == 'list':
            return AnnouncementListSerializer
        elif self.action == 'retrieve':
            return AnnouncementDetailSerializer
        return AnnouncementSerializer

    def get_queryset(self):
        """普通用户只能看到已发布且未过期的公告"""
        user = self.request.user
        now = timezone.now()

        if user.is_authenticated and (user.is_superuser or user.user_type in ['admin', 'organizer']):
            return self.queryset

        # 普通用户只能看到已发布且未过期的公告
        return self.queryset.filter(
            is_published=True
        ).filter(
            models.Q(expire_time__isnull=True) | models.Q(expire_time__gte=now)
        )

    def retrieve(self, request, *args, **kwargs):
        """获取公告详情并增加浏览次数"""
        instance = self.get_object()
        instance.view_count += 1
        instance.save(update_fields=['view_count'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def published(self, request):
        """
        获取已发布的公告
        GET /api/announcements/published/
        """
        now = timezone.now()
        announcements = self.queryset.filter(
            is_published=True
        ).filter(
            models.Q(expire_time__isnull=True) | models.Q(expire_time__gte=now)
        ).order_by('-is_pinned', '-publish_time')

        serializer = AnnouncementListSerializer(announcements, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def pinned(self, request):
        """
        获取置顶公告
        GET /api/announcements/pinned/
        """
        now = timezone.now()
        announcements = self.queryset.filter(
            is_published=True,
            is_pinned=True
        ).filter(
            models.Q(expire_time__isnull=True) | models.Q(expire_time__gte=now)
        ).order_by('-publish_time')

        serializer = AnnouncementListSerializer(announcements, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['put', 'post'])
    def publish(self, request, pk=None):
        """
        发布公告
        PUT /api/announcements/{id}/publish/
        """
        announcement = self.get_object()
        announcement.is_published = True
        if not announcement.publish_time:
            announcement.publish_time = timezone.now()
        announcement.save()

        return Response({
            'message': '公告已发布',
            'announcement': AnnouncementSerializer(announcement).data
        })

    @action(detail=True, methods=['put'])
    def unpublish(self, request, pk=None):
        """
        取消发布公告
        PUT /api/announcements/{id}/unpublish/
        """
        announcement = self.get_object()
        announcement.is_published = False
        announcement.save()

        return Response({
            'message': '公告已取消发布',
            'announcement': AnnouncementSerializer(announcement).data
        })

    @action(detail=True, methods=['put'])
    def pin(self, request, pk=None):
        """
        置顶公告
        PUT /api/announcements/{id}/pin/
        """
        announcement = self.get_object()
        announcement.is_pinned = True
        announcement.save()

        return Response({
            'message': '公告已置顶',
            'announcement': AnnouncementSerializer(announcement).data
        })

    @action(detail=True, methods=['put'])
    def unpin(self, request, pk=None):
        """
        取消置顶公告
        PUT /api/announcements/{id}/unpin/
        """
        announcement = self.get_object()
        announcement.is_pinned = False
        announcement.save()

        return Response({
            'message': '公告已取消置顶',
            'announcement': AnnouncementSerializer(announcement).data
        })

    @action(detail=False, methods=['post'])
    def upload_image(self, request):
        """
        上传公告封面图片到前端public目录
        POST /api/announcements/upload_image/
        """
        # el-upload 默认使用 'file' 字段名
        if 'file' not in request.FILES and 'image' not in request.FILES:
            return Response({
                'error': '请上传图片文件'
            }, status=status.HTTP_400_BAD_REQUEST)

        image_file = request.FILES.get('file') or request.FILES.get('image')

        allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp']
        if image_file.content_type not in allowed_types:
            return Response({
                'error': '只支持 jpg, png, gif, webp 格式的图片'
            }, status=status.HTTP_400_BAD_REQUEST)

        if image_file.size > 5 * 1024 * 1024:
            return Response({
                'error': '图片大小不能超过 5MB'
            }, status=status.HTTP_400_BAD_REQUEST)

        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        random_str = str(uuid.uuid4())[:8]
        extension = image_file.name.split('.')[-1]
        filename = f'announcement_{timestamp}_{random_str}.{extension}'

        frontend_public_dir = os.path.join(settings.BASE_DIR, '..', 'frontend', 'public', 'images', 'announcements')
        os.makedirs(frontend_public_dir, exist_ok=True)

        file_path = os.path.join(frontend_public_dir, filename)
        with open(file_path, 'wb+') as destination:
            for chunk in image_file.chunks():
                destination.write(chunk)

        relative_path = f'/images/announcements/{filename}'

        return Response({
            'message': '图片上传成功',
            'image': relative_path
        })


# 导入models用于Q查询
from django.db import models
