"""
互动应用URL路由
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LikeViewSet, FavoriteViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'likes', LikeViewSet, basename='like')
router.register(r'favorites', FavoriteViewSet, basename='favorite')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
]
