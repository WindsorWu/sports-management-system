"""
WebSocket 路由配置模块

本模块定义了应用的 WebSocket 路由规则，类似于 HTTP 的 urls.py。
将 WebSocket URL 模式映射到对应的消费者（Consumer）处理类。

配置说明：
    Django Channels 使用路由配置来决定不同的 WebSocket 连接
    应该由哪个消费者来处理。本模块配置的路由会被项目的
    主 ASGI 配置文件（asgi.py）引用。
"""

from django.urls import re_path

from .consumers import CommentWordCloudConsumer

# WebSocket URL 模式列表
websocket_urlpatterns = [
    # 评论词云 WebSocket 路由
    # URL: ws://host/ws/comments/wordcloud/
    # 说明：管理后台的数据大屏通过此 WebSocket 连接接收实时词云数据
    # 消费者：CommentWordCloudConsumer 负责处理此路由的所有连接
    re_path(r"ws/comments/wordcloud/", CommentWordCloudConsumer.as_asgi()),
]
