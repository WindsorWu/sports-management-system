import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .comment_wordcloud import collect_wordcloud_data, WORDCLOUD_GROUP


class CommentWordCloudConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(WORDCLOUD_GROUP, self.channel_name)
        await self.accept()

        payload = await database_sync_to_async(collect_wordcloud_data)()
        await self.send(text_data=json.dumps({
            "type": "wordcloud_update",
            "payload": payload,
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(WORDCLOUD_GROUP, self.channel_name)

    async def wordcloud_update(self, event):
        await self.send(text_data=json.dumps({
            "type": "wordcloud_update",
            "payload": event["payload"],
        }))
