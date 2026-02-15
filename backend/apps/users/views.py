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
    UserProfileUpdateSerializer,
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
        """
        动态设置视图的权限类
        
        根据不同的action（操作类型）返回不同的权限要求
        这是DRF ViewSet的一个重要特性，可以为不同操作设置不同的权限
        
        权限配置说明:
            - register: 注册接口，允许任何人访问（未登录用户也可注册）
            - me, update_profile, change_password: 需要用户已登录
            - list, retrieve: 用户列表和详情，允许任何人查看
            - update, partial_update, destroy: 只有所有者或管理员可以操作
            - 其他操作: 需要管理员权限
            
        返回:
            list: 权限类实例列表
        """
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
        """
        动态返回序列化器类
        
        根据不同的action返回最适合该操作的序列化器
        这样可以为不同的操作提供不同的字段集和验证规则
        
        序列化器选择逻辑:
            - register: 使用注册专用序列化器（包含密码验证）
            - me: 使用详细的个人信息序列化器
            - update_profile: 使用个人信息更新序列化器（只允许修改部分字段）
            - change_password: 使用修改密码序列化器
            - 其他: 使用通用的用户序列化器
            
        返回:
            Serializer类: 对应操作的序列化器类
        """
        if self.action == 'register':
            return UserRegisterSerializer
        elif self.action == 'me':
            return UserProfileSerializer
        elif self.action == 'update_profile':
            return UserProfileUpdateSerializer
        elif self.action == 'change_password':
            return ChangePasswordSerializer
        return UserSerializer

    @action(detail=False, methods=['post'])
    def register(self, request):
        """
        用户注册接口
        
        接收用户提交的注册信息，创建新用户账号
        不需要认证即可访问，任何人都可以注册
        
        请求方法: POST
        URL: /api/users/register/
        
        请求参数:
            - username: 用户名（必填）
            - email: 邮箱（必填）
            - password: 密码（必填）
            - password_confirm: 确认密码（必填）
            - real_name: 真实姓名（必填）
            - phone: 手机号（必填）
            - user_type: 用户类型（必填，可选值：athlete/organizer/referee/admin）
        
        返回数据:
            - 成功: HTTP 201，包含消息和新用户信息
            - 失败: HTTP 400，包含验证错误信息
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # 验证数据，失败则抛出异常
        user = serializer.save()                    # 创建用户
        return Response({
            'message': '注册成功',
            'user': UserSerializer(user).data       # 返回新用户的基本信息
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def me(self, request):
        """
        获取当前登录用户信息接口
        
        返回当前已认证用户的完整个人信息
        需要用户已登录（提供有效的JWT token）
        
        请求方法: GET
        URL: /api/users/me/
        
        请求头:
            Authorization: Bearer <access_token>
        
        返回数据:
            - 成功: HTTP 200，包含用户详细信息
            - 失败: HTTP 401，未认证
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['put', 'patch'])
    def update_profile(self, request):
        """
        更新当前用户信息接口
        
        允许用户更新自己的部分个人信息
        支持完整更新（PUT）和部分更新（PATCH）
        
        请求方法: PUT 或 PATCH
        URL: /api/users/update_profile/
        
        请求头:
            Authorization: Bearer <access_token>
        
        请求参数（可选，只更新提供的字段）:
            - username: 用户名
            - email: 邮箱
            - phone: 手机号
        
        返回数据:
            - 成功: HTTP 200，包含更新后的用户信息
            - 失败: HTTP 400，包含验证错误信息
        """
        serializer = self.get_serializer(
            request.user,
            data=request.data,
            partial=True  # 允许部分更新，不需要提供所有字段
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
        修改密码接口
        
        允许用户修改自己的登录密码
        需要提供旧密码进行验证，确保安全性
        
        请求方法: POST
        URL: /api/users/change_password/
        
        请求头:
            Authorization: Bearer <access_token>
        
        请求参数:
            - old_password: 当前密码（必填）
            - new_password: 新密码（必填）
            - new_password_confirm: 确认新密码（必填）
        
        返回数据:
            - 成功: HTTP 200，包含成功消息
            - 失败: HTTP 400，包含错误信息（如旧密码错误、新密码格式不正确等）
            
        注意: 密码修改成功后，之前的token仍然有效，用户无需重新登录
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 设置新密码（使用set_password方法会自动加密）
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()

        return Response({
            'message': '密码修改成功'
        })

    @action(detail=True, methods=['get'])
    def registrations(self, request, pk=None):
        """
        获取指定用户的报名记录接口
        
        查询指定用户参与的所有赛事报名记录
        使用select_related优化查询性能，避免N+1问题
        
        请求方法: GET
        URL: /api/users/{id}/registrations/
        
        URL参数:
            - id: 用户ID
        
        返回数据:
            - 成功: HTTP 200，包含用户的所有报名记录列表
            - 失败: HTTP 404，用户不存在
            
        返回字段包括:
            报名ID、赛事信息、报名状态、报名时间等
        """
        user = self.get_object()  # 获取指定ID的用户对象
        # select_related预加载外键关联的event对象，减少数据库查询次数
        registrations = user.registrations.select_related('event').all()

        # 导入序列化器（避免循环导入）
        from apps.registrations.serializers import RegistrationSerializer
        serializer = RegistrationSerializer(registrations, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def results(self, request, pk=None):
        """
        获取指定用户的成绩记录接口
        
        查询指定用户在各个赛事中的成绩记录
        使用select_related优化查询，一次性加载关联的赛事和报名信息
        
        请求方法: GET
        URL: /api/users/{id}/results/
        
        URL参数:
            - id: 用户ID
        
        返回数据:
            - 成功: HTTP 200，包含用户的所有成绩记录列表
            - 失败: HTTP 404，用户不存在
            
        返回字段包括:
            成绩ID、赛事信息、比赛轮次、排名、成绩、发布状态等
        """
        user = self.get_object()
        # select_related同时加载event和registration，优化查询性能
        results = user.results.select_related('event', 'registration').all()

        from apps.results.serializers import ResultSerializer
        serializer = ResultSerializer(results, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['put'])
    def activate(self, request, pk=None):
        """
        启用用户账号接口
        
        将用户账号设置为激活状态，允许用户登录和使用系统
        需要管理员权限
        
        请求方法: PUT
        URL: /api/users/{id}/activate/
        
        URL参数:
            - id: 用户ID
        
        请求头:
            Authorization: Bearer <admin_access_token>
        
        返回数据:
            - 成功: HTTP 200，包含成功消息和更新后的用户信息
            - 失败: HTTP 403，权限不足；HTTP 404，用户不存在
        """
        user = self.get_object()
        user.is_active = True
        user.save()

        return Response({
            'message': '用户已启用',
            'user': UserSerializer(user).data
        })

    @action(detail=True, methods=['put'])
    def deactivate(self, request, pk=None):
        """
        禁用用户账号接口
        
        将用户账号设置为禁用状态，禁止用户登录
        需要管理员权限，但不允许禁用超级管理员账户（安全保护）
        
        请求方法: PUT
        URL: /api/users/{id}/deactivate/
        
        URL参数:
            - id: 用户ID
        
        请求头:
            Authorization: Bearer <admin_access_token>
        
        返回数据:
            - 成功: HTTP 200，包含成功消息和更新后的用户信息
            - 失败: HTTP 400，尝试禁用超级管理员；HTTP 403，权限不足；HTTP 404，用户不存在
            
        安全限制:
            - 不允许禁用超级管理员账户，防止系统无法管理
        """
        user = self.get_object()

        # 不允许禁用超级管理员（安全保护）
        if user.is_superuser:
            return Response({
                'error': '不能禁用超级管理员账户'
            }, status=status.HTTP_400_BAD_REQUEST)

        user.is_active = False
        user.save()

        return Response({
            'message': '用户已禁用',
            'user': UserSerializer(user).data
        })
