"""
轮播图应用序列化器
"""
from rest_framework import serializers
from .models import Carousel


class CarouselSerializer(serializers.ModelSerializer):
    """轮播图序列化器"""
    creator_name = serializers.CharField(source='creator.real_name', read_only=True)
    event_title = serializers.CharField(source='event.title', read_only=True)

    class Meta:
        model = Carousel
        fields = [
            'id', 'title', 'description', 'image', 'link_url', 'event',
            'event_title', 'position', 'order', 'is_active', 'start_time',
            'end_time', 'click_count', 'creator', 'creator_name',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'creator', 'click_count', 'created_at', 'updated_at', 'creator_name', 'event_title']

    def create(self, validated_data):
        """创建轮播图时自动设置创建者"""
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)


class CarouselListSerializer(serializers.ModelSerializer):
    """轮播图列表序列化器（简化版）"""
    event_title = serializers.CharField(source='event.title', read_only=True)

    class Meta:
        model = Carousel
        fields = [
            'id', 'title', 'image', 'link_url', 'event_title',
            'position', 'order', 'is_active', 'created_at'
        ]
