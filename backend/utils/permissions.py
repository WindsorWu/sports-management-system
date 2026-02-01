"""
权限控制类
定义不同角色的权限
"""
from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """管理员权限"""

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_superuser


class IsReferee(permissions.BasePermission):
    """裁判权限（实际为组织者）"""

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.user_type == 'organizer'


class IsAthlete(permissions.BasePermission):
    """运动员权限"""

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.user_type == 'athlete'


class IsAdminOrReferee(permissions.BasePermission):
    """管理员或裁判权限（实际为管理员或组织者）"""

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (
            request.user.is_superuser or request.user.user_type in ['admin', 'organizer', 'referee']
        )


class IsOwnerOrAdmin(permissions.BasePermission):
    """所有者或管理员权限"""

    def has_object_permission(self, request, view, obj):
        # 管理员拥有所有权限
        if request.user.is_superuser:
            return True
        if request.user.user_type == 'admin' and getattr(obj, 'user_type', None) == 'referee':
            return True
        if request.user.is_staff and getattr(obj, 'is_staff', False):
            return True
        # 对象的所有者
        if hasattr(obj, 'user'):
            return obj.user == request.user
        elif hasattr(obj, 'created_by'):
            return obj.created_by == request.user
        return False


class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """
    认证用户可以进行任何操作，未认证用户只能读取
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated


class IsSuperAdminOrAdminRole(permissions.BasePermission):
    """超级管理员或 admin 角色"""

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (
            request.user.is_superuser or request.user.user_type == 'admin'
        )

