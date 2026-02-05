"""
WebSocket 消费者模块

本模块定义了处理词云 WebSocket 连接的消费者类。
前端通过 WebSocket 连接到服务器，可以实时接收词云数据的更新。
"""

import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .comment_wordcloud import collect_wordcloud_data, WORDCLOUD_GROUP


class CommentWordCloudConsumer(AsyncWebsocketConsumer):
    """
    评论词云 WebSocket 消费者
    
    功能说明：
        这是一个异步 WebSocket 消费者，负责处理前端（管理后台）与后端之间的
        词云数据实时通信。当管理员打开数据大屏时，前端会建立 WebSocket 连接，
        实时接收评论词云的更新。
        
    连接流程：
        1. 前端连接 ws://host/ws/comments/wordcloud/
        2. 服务器将连接加入词云频道组（WORDCLOUD_GROUP）
        3. 立即发送当前的词云数据给客户端
        4. 后续当有评论变动时，通过 wordcloud_update 方法推送更新
        5. 断开连接时，从频道组中移除
        
    数据格式：
        发送给客户端的消息格式：
        {
            "type": "wordcloud_update",
            "payload": [{"text": "词汇", "weight": 频率}, ...]
        }
    """
    
    async def connect(self):
        """
        处理 WebSocket 连接建立
        
        工作流程：
            1. 将当前连接加入词云频道组（WORDCLOUD_GROUP）
               这样当有词云更新时，这个连接就能收到广播消息
            2. 接受 WebSocket 连接（完成握手）
            3. 立即获取并发送当前的词云数据给客户端
               确保客户端连接后能立即看到最新的词云
               
        注意：
            collect_wordcloud_data() 是同步函数（涉及数据库查询），
            需要使用 database_sync_to_async 包装后在异步环境中调用
        """
        # 将当前连接加入词云频道组
        await self.channel_layer.group_add(WORDCLOUD_GROUP, self.channel_name)
        
        # 接受 WebSocket 连接
        await self.accept()

        # 获取当前词云数据（同步函数需要包装为异步）
        payload = await database_sync_to_async(collect_wordcloud_data)()
        
        # 立即发送当前词云数据给刚连接的客户端
        await self.send(text_data=json.dumps({
            "type": "wordcloud_update",
            "payload": payload,
        }))

    async def disconnect(self, close_code):
        """
        处理 WebSocket 连接断开
        
        Args:
            close_code: WebSocket 关闭状态码
            
        说明：
            当客户端断开连接时（如关闭浏览器标签页），
            将该连接从词云频道组中移除，避免向已断开的连接发送消息
        """
        # 从词云频道组中移除当前连接
        await self.channel_layer.group_discard(WORDCLOUD_GROUP, self.channel_name)

    async def wordcloud_update(self, event):
        """
        处理词云更新消息
        
        Args:
            event: 从频道层接收到的事件字典，包含：
                   - type: 消息类型（"wordcloud_update"）
                   - payload: 词云数据列表
                   
        说明：
            当评论发生变化时，signals.py 中的信号处理器会调用
            broadcast_comment_wordcloud() 函数，该函数通过 group_send
            向 WORDCLOUD_GROUP 组发送消息。
            
            消息的 type 为 "wordcloud.update"（带点），Django Channels
            会自动将点转换为下划线，并调用对应的方法（即本方法）。
            
            本方法接收到消息后，将其转发给 WebSocket 客户端。
            
        工作流程：
            1. 从 event 中提取词云数据
            2. 通过 WebSocket 发送给客户端
            3. 前端收到数据后更新词云图表显示
        """
        # 将词云更新消息发送给 WebSocket 客户端
        await self.send(text_data=json.dumps({
            "type": "wordcloud_update",
            "payload": event["payload"],
        }))
