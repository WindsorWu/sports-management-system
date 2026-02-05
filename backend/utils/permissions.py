"""
权限控制类
定义不同角色的权限
"""
from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """
    管理员权限类
    
    用于限制只有超级管理员才能访问的接口
    通过检查用户的is_superuser属性来判断
    
    返回:
        bool: 用户是超级管理员时返回True，否则返回False
    """

    def has_permission(self, request, view):
        """
        检查用户是否有管理员权限
        
        参数:
            request: HTTP请求对象，包含当前用户信息
            view: 视图对象
            
        返回:
            bool: 用户已认证且是超级管理员时返回True
        """
        return request.user and request.user.is_authenticated and request.user.is_superuser


class IsReferee(permissions.BasePermission):
    """
    裁判权限类（实际为组织者）
    
    用于限制只有组织者角色才能访问的接口
    注意：虽然类名为IsReferee，但实际检查的是organizer类型
    
    返回:
        bool: 用户是组织者时返回True，否则返回False
    """

    def has_permission(self, request, view):
        """
        检查用户是否有裁判/组织者权限
        
        参数:
            request: HTTP请求对象，包含当前用户信息
            view: 视图对象
            
        返回:
            bool: 用户已认证且user_type为organizer时返回True
        """
        return request.user and request.user.is_authenticated and request.user.user_type == 'organizer'


class IsAthlete(permissions.BasePermission):
    """
    运动员权限类
    
    用于限制只有运动员角色才能访问的接口
    
    返回:
        bool: 用户是运动员时返回True，否则返回False
    """

    def has_permission(self, request, view):
        """
        检查用户是否有运动员权限
        
        参数:
            request: HTTP请求对象，包含当前用户信息
            view: 视图对象
            
        返回:
            bool: 用户已认证且user_type为athlete时返回True
        """
        return request.user and request.user.is_authenticated and request.user.user_type == 'athlete'


class IsAdminOrReferee(permissions.BasePermission):
    """
    管理员或裁判权限类（实际为管理员或组织者）
    
    用于限制只有管理员、组织者或裁判角色才能访问的接口
    适用于需要管理权限但不要求超级管理员的场景
    
    返回:
        bool: 用户是管理员、组织者或裁判时返回True
    """

    def has_permission(self, request, view):
        """
        检查用户是否有管理员或裁判权限
        
        参数:
            request: HTTP请求对象，包含当前用户信息
            view: 视图对象
            
        返回:
            bool: 用户已认证且是超级管理员或user_type为admin/organizer/referee时返回True
        """
        return request.user and request.user.is_authenticated and (
            request.user.is_superuser or request.user.user_type in ['admin', 'organizer', 'referee']
        )


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    所有者或管理员权限类
    
    用于对象级别的权限控制，允许对象所有者或管理员访问
    适用于用户只能操作自己创建的资源的场景
    
    权限规则:
        1. 超级管理员拥有所有权限
        2. admin角色可以管理referee类型的对象
        3. staff用户可以管理staff对象
        4. 对象的创建者可以管理自己创建的对象
    """

    def has_object_permission(self, request, view, obj):
        """
        检查用户是否有访问特定对象的权限
        
        参数:
            request: HTTP请求对象，包含当前用户信息
            view: 视图对象
            obj: 要访问的数据库对象
            
        返回:
            bool: 用户有权限访问该对象时返回True
        """
        # 管理员拥有所有权限
        if request.user.is_superuser:
            return True
        # admin角色可以管理referee用户
        if request.user.user_type == 'admin' and getattr(obj, 'user_type', None) == 'referee':
            return True
        # staff用户可以管理staff对象
        if request.user.is_staff and getattr(obj, 'is_staff', False):
            return True
        # 对象的所有者（通过user字段关联）
        if hasattr(obj, 'user'):
            return obj.user == request.user
        # 对象的创建者（通过created_by字段关联）
        elif hasattr(obj, 'created_by'):
            return obj.created_by == request.user
        return False


class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """
    认证用户可以进行任何操作，未认证用户只能读取
    
    这是一个常用的权限类，允许：
    - 未认证用户：只能进行GET、HEAD、OPTIONS等安全方法（只读）
    - 已认证用户：可以进行POST、PUT、PATCH、DELETE等写操作
    
    适用场景：公开内容的查看，但修改需要登录
    """

    def has_permission(self, request, view):
        """
        检查用户是否有权限执行当前操作
        
        参数:
            request: HTTP请求对象，包含请求方法和用户信息
            view: 视图对象
            
        返回:
            bool: 读操作总是返回True，写操作需要用户已认证
        """
        # 如果是安全方法（GET、HEAD、OPTIONS），允许任何人访问
        if request.method in permissions.SAFE_METHODS:
            return True
        # 其他方法（POST、PUT、PATCH、DELETE）需要用户已认证
        return request.user and request.user.is_authenticated


class IsSuperAdminOrAdminRole(permissions.BasePermission):
    """
    超级管理员或admin角色权限类
    
    用于限制只有超级管理员或admin用户类型才能访问的接口
    比IsAdmin权限更宽松，不仅检查is_superuser，还允许user_type为admin的用户
    
    适用场景：需要管理权限但不必是系统超级管理员的功能
    """

    def has_permission(self, request, view):
        """
        检查用户是否是超级管理员或admin角色
        
        参数:
            request: HTTP请求对象，包含当前用户信息
            view: 视图对象
            
        返回:
            bool: 用户是超级管理员或user_type为admin时返回True
        """
        return request.user and request.user.is_authenticated and (
            request.user.is_superuser or request.user.user_type == 'admin'
        )

