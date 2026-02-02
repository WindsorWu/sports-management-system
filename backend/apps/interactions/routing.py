from django.urls import re_path

from .consumers import CommentWordCloudConsumer

websocket_urlpatterns = [
    re_path(r"ws/comments/wordcloud/", CommentWordCloudConsumer.as_asgi()),
]
