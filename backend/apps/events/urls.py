"""
赛事应用URL路由
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, EventAssignmentViewSet

router = DefaultRouter()
router.register(r'', EventViewSet, basename='event')
router.register(r'assignments', EventAssignmentViewSet, basename='eventassignment')

urlpatterns = [
    path('', include(router.urls)),
]
