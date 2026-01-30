"""
用户应用视图
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import User
from .serializers import (
    UserSerializer,
    UserRegisterSerializer,
    UserProfileSerializer,
    ChangePasswordSerializer
)
from utils.permissions import IsAdmin, IsOwnerOrAdmin


class UserViewSet(viewsets.ModelViewSet):
    """
    用户视图集
    提供用户的CRUD操作
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['user_type', 'is_verified', 'is_active', 'gender']
    search_fields = ['username', 'real_name', 'phone', 'email', 'organization']
    ordering_fields = ['created_at', 'username']
    ordering = ['-created_at']

    def get_permissions(self):
        """设置权限"""
        if self.action == 'register':
            # 注册接口允许任何人访问
            permission_classes = [AllowAny]
        elif self.action in ['me', 'update_profile', 'change_password']:
            # 个人信息接口需要认证
            permission_classes = [IsAuthenticated]
        elif self.action in ['list', 'retrieve']:
            # 列表和详情允许只读
            permission_classes = [AllowAny]
        elif self.action in ['update', 'partial_update', 'destroy']:
            # 更新和删除需要是所有者或管理员
            permission_classes = [IsOwnerOrAdmin]
        else:
            # 其他操作需要管理员权限
            permission_classes = [IsAdmin]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        """根据不同操作返回不同的序列化器"""
        if self.action == 'register':
            return UserRegisterSerializer
        elif self.action in ['me', 'update_profile']:
            return UserProfileSerializer
        elif self.action == 'change_password':
            return ChangePasswordSerializer
        return UserSerializer

    @action(detail=False, methods=['post'])
    def register(self, request):
        """
        用户注册
        POST /api/users/register/
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'message': '注册成功',
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def me(self, request):
        """
        获取当前用户信息
        GET /api/users/me/
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['put', 'patch'])
    def update_profile(self, request):
        """
        更新当前用户信息
        PUT/PATCH /api/users/update_profile/
        """
        serializer = self.get_serializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message': '个人信息更新成功',
            'user': serializer.data
        })

    @action(detail=False, methods=['post'])
    def change_password(self, request):
        """
        修改密码
        POST /api/users/change_password/
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 设置新密码
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()

        return Response({
            'message': '密码修改成功'
        })

    @action(detail=True, methods=['get'])
    def registrations(self, request, pk=None):
        """
        获取用户的报名记录
        GET /api/users/{id}/registrations/
        """
        user = self.get_object()
        registrations = user.registrations.select_related('event').all()

        from apps.registrations.serializers import RegistrationSerializer
        serializer = RegistrationSerializer(registrations, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def results(self, request, pk=None):
        """
        获取用户的成绩记录
        GET /api/users/{id}/results/
        """
        user = self.get_object()
        results = user.results.select_related('event', 'registration').all()

        from apps.results.serializers import ResultSerializer
        serializer = ResultSerializer(results, many=True)
        return Response(serializer.data)
