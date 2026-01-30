"""
成绩应用URL路由
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ResultViewSet

router = DefaultRouter()
router.register(r'', ResultViewSet, basename='result')

urlpatterns = [
    path('', include(router.urls)),
]
