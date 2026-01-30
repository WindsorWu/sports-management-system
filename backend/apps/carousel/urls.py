"""
轮播图应用URL路由
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CarouselViewSet

router = DefaultRouter()
router.register(r'', CarouselViewSet, basename='carousel')

urlpatterns = [
    path('', include(router.urls)),
]
