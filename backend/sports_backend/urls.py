"""
URL configuration for sports_backend project.

主路由配置 - 运动赛事管理与报名系统
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    # Django管理后台
    path("admin/", admin.site.urls),

    # JWT认证接口
    path('api/auth/', include([
        path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        path('verify/', TokenVerifyView.as_view(), name='token_verify'),
    ])),

    # 用户管理
    path('api/users/', include('apps.users.urls')),

    # 赛事管理
    path('api/events/', include('apps.events.urls')),

    # 报名管理
    path('api/registrations/', include('apps.registrations.urls')),

    # 成绩管理
    path('api/results/', include('apps.results.urls')),

    # 公告管理
    path('api/announcements/', include('apps.announcements.urls')),

    # 互动功能（点赞、收藏、评论）
    path('api/interactions/', include('apps.interactions.urls')),

    # 轮播图管理
    path('api/carousels/', include('apps.carousel.urls')),

    # 反馈管理
    path('api/feedbacks/', include('apps.feedback.urls')),
]

# 开发环境下提供媒体文件服务
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
