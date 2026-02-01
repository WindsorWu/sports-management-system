"""
互动应用视图（点赞、收藏、评论）
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.contrib.contenttypes.models import ContentType
from rest_framework.exceptions import ValidationError
import logging
from django.db import IntegrityError

from .models import Like, Favorite, Comment
from .serializers import (
    LikeSerializer,
    FavoriteSerializer,
    CommentSerializer,
    CommentCreateSerializer
)
from utils.permissions import IsOwnerOrAdmin, IsAdmin


logger = logging.getLogger(__name__)


def normalize_interaction_payload(data):
    payload = data.copy()
    target_type = payload.pop('target_type', None)
    target_id = payload.pop('target_id', None)

    if 'content_type' not in payload:
        if not target_type:
            raise ValidationError({'content_type': 'content_type 或 target_type 必须提供'})
        model_name = target_type.split('.')[-1].lower()
        try:
            content_type = ContentType.objects.get(model=model_name)
        except ContentType.DoesNotExist:
            raise ValidationError({'target_type': '无效的 target_type'})
        payload['content_type'] = content_type.id

    if 'object_id' not in payload:
        if target_id is None:
            raise ValidationError({'object_id': 'object_id 或 target_id 必须提供'})
        try:
            payload['object_id'] = int(target_id)
        except (TypeError, ValueError):
            raise ValidationError({'target_id': 'target_id 必须是整数'})

    return payload


class LikeViewSet(viewsets.ModelViewSet):
    """
    点赞视图集
    """
    queryset = Like.objects.select_related('user', 'content_type').all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['content_type', 'object_id']
    ordering = ['-created_at']

    def get_queryset(self):
        """只返回当前用户的点赞"""
        return self.queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """点赞"""
        payload = normalize_interaction_payload(request.data)
        content_type_id = payload.get('content_type')
        object_id = payload.get('object_id')

        # 检查是否已经点赞
        if Like.objects.filter(
            user=request.user,
            content_type_id=content_type_id,
            object_id=object_id
        ).exists():
            return Response({
                'error': '您已经点赞过了'
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=payload)
        serializer.is_valid(raise_exception=True)
        like = serializer.save()

        return Response({
            'message': '点赞成功',
            'like': LikeSerializer(like).data
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def unlike(self, request):
        """
        取消点赞
        POST /api/interactions/likes/unlike/
        Body: {content_type: id, object_id: id}
        """
        payload = normalize_interaction_payload(request.data)
        content_type_id = payload.get('content_type')
        object_id = payload.get('object_id')

        like = Like.objects.filter(
            user=request.user,
            content_type_id=content_type_id,
            object_id=object_id
        ).first()

        if not like:
            return Response({
                'error': '未找到点赞记录'
            }, status=status.HTTP_404_NOT_FOUND)

        like.delete()

        return Response({
            'message': '取消点赞成功'
        })

    @action(detail=False, methods=['get'])
    def check(self, request):
        """
        检查是否已点赞
        GET /api/interactions/likes/check/?content_type={id}&object_id={id}
        """
        payload = normalize_interaction_payload(request.query_params)
        liked = Like.objects.filter(
            user=request.user,
            content_type_id=payload.get('content_type'),
            object_id=payload.get('object_id')
        ).exists()

        return Response({
            'liked': liked
        })


class FavoriteViewSet(viewsets.ModelViewSet):
    """
    收藏视图集
    """
    queryset = Favorite.objects.select_related('user', 'content_type').all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['content_type', 'object_id']
    search_fields = ['remarks']
    ordering = ['-created_at']

    def get_queryset(self):
        """只返回当前用户的收藏"""
        return self.queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """收藏"""
        payload = normalize_interaction_payload(request.data)
        content_type_id = payload.get('content_type')
        object_id = payload.get('object_id')

        # 检查是否已经收藏
        if Favorite.objects.filter(
            user=request.user,
            content_type_id=content_type_id,
            object_id=object_id
        ).exists():
            return Response({
                'error': '您已经收藏过了'
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=payload)
        serializer.is_valid(raise_exception=True)
        try:
            favorite = serializer.save()
        except IntegrityError:
            logger.warning('Favorite duplicated? user=%s payload=%s', request.user.id, payload)
            return Response({
                'error': '您已经收藏过了'
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as exc:
            logger.exception('收藏过程中出错 user=%s payload=%s', request.user.id, payload)
            return Response({
                'error': '收藏失败，请稍后再试'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({
            'message': '收藏成功',
            'favorite': FavoriteSerializer(favorite).data
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def unfavorite(self, request):
        """
        取消收藏
        POST /api/interactions/favorites/unfavorite/
        Body: {content_type: id, object_id: id}
        """
        payload = normalize_interaction_payload(request.data)
        content_type_id = payload.get('content_type')
        object_id = payload.get('object_id')

        favorite = Favorite.objects.filter(
            user=request.user,
            content_type_id=content_type_id,
            object_id=object_id
        ).first()

        if not favorite:
            return Response({
                'error': '未找到收藏记录'
            }, status=status.HTTP_404_NOT_FOUND)

        favorite.delete()

        return Response({
            'message': '取消收藏成功'
        })

    @action(detail=False, methods=['get'])
    def check(self, request):
        """
        检查是否已收藏
        GET /api/interactions/favorites/check/?content_type={id}&object_id={id}
        """
        payload = normalize_interaction_payload(request.query_params)
        favorited = Favorite.objects.filter(
            user=request.user,
            content_type_id=payload.get('content_type'),
            object_id=payload.get('object_id')
        ).exists()

        return Response({
            'favorited': favorited
        })


class CommentViewSet(viewsets.ModelViewSet):
    """
    评论视图集
    """
    queryset = Comment.objects.select_related('user', 'content_type', 'parent', 'reply_to').prefetch_related('replies').all()
    serializer_class = CommentSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['content_type', 'object_id', 'is_approved', 'parent']
    search_fields = ['content', 'user__username', 'user__real_name']
    ordering = ['-created_at']

    def get_permissions(self):
        """设置权限"""
        if self.action in ['list', 'retrieve']:
            # 列表和详情允许任何人访问
            permission_classes = [AllowAny]
        elif self.action == 'create':
            # 创建评论需要认证
            permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update', 'destroy']:
            # 更新和删除需要是所有者或管理员
            permission_classes = [IsOwnerOrAdmin]
        elif self.action in ['approve', 'reject']:
            # 审核需要管理员权限
            permission_classes = [IsAdmin]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        """根据不同操作返回不同的序列化器"""
        if self.action == 'create':
            return CommentCreateSerializer
        return CommentSerializer

    def get_queryset(self):
        """普通用户只能看到已审核的评论"""
        user = self.request.user
        if user.is_authenticated and (user.is_superuser or user.user_type == 'admin'):
            return self.queryset
        return self.queryset.filter(is_approved=True)

    def create(self, request, *args, **kwargs):
        """创建评论"""
        payload = normalize_interaction_payload(request.data)
        serializer = self.get_serializer(data=payload)
        serializer.is_valid(raise_exception=True)
        comment = serializer.save()

        return Response({
            'message': '评论成功',
            'comment': CommentSerializer(comment).data
        }, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['put'])
    def approve(self, request, pk=None):
        """
        审核通过
        PUT /api/interactions/comments/{id}/approve/
        """
        comment = self.get_object()
        comment.is_approved = True
        comment.save()

        return Response({
            'message': '评论已通过审核',
            'comment': CommentSerializer(comment).data
        })

    @action(detail=True, methods=['put'])
    def reject(self, request, pk=None):
        """
        审核拒绝
        PUT /api/interactions/comments/{id}/reject/
        """
        comment = self.get_object()
        comment.is_approved = False
        comment.save()

        return Response({
            'message': '评论已拒绝',
            'comment': CommentSerializer(comment).data
        })

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        """
        点赞评论
        POST /api/interactions/comments/{id}/like/
        """
        comment = self.get_object()
        comment.like_count += 1
        comment.save()

        return Response({
            'message': '点赞成功',
            'like_count': comment.like_count
        })
