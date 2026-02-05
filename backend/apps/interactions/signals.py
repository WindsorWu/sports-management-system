"""
评论信号处理模块

本模块通过 Django 信号机制监听评论的创建、更新和删除事件，
并在评论发生变化时自动触发词云数据的重新计算和广播。

信号机制说明：
    Django 信号是一种观察者模式的实现，当特定事件发生时，
    信号会自动调用已注册的处理函数。
    
本模块使用的信号：
    - post_save: 模型保存后触发（包括创建和更新）
    - post_delete: 模型删除后触发
"""

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Comment
from .comment_wordcloud import broadcast_comment_wordcloud


@receiver(post_save, sender=Comment)
def handle_comment_save(sender, instance, **kwargs):
    """
    处理评论保存后的信号（创建或更新）
    
    Args:
        sender: 发送信号的模型类（Comment）
        instance: 被保存的评论实例
        **kwargs: 其他参数，可能包含：
                 - created: 布尔值，True 表示新创建，False 表示更新
                 - using: 使用的数据库别名
                 - update_fields: 更新的字段列表
                 
    触发时机：
        - 新评论被创建时
        - 现有评论被更新时（如审核状态变更）
        
    处理逻辑：
        只有当评论已审核通过（is_approved=True）时，才广播词云更新。
        这样可以避免未审核的评论影响词云显示，同时也能减少不必要的广播。
        
    说明：
        当管理员审核通过一条新评论时，评论的 is_approved 字段会被设置为 True，
        此时信号被触发，词云数据会重新计算并推送给所有连接的管理后台客户端。
    """
    # 只处理已审核通过的评论
    if not instance.is_approved:
        return
    
    # 广播词云数据更新
    broadcast_comment_wordcloud()


@receiver(post_delete, sender=Comment)
def handle_comment_delete(sender, instance, **kwargs):
    """
    处理评论删除后的信号
    
    Args:
        sender: 发送信号的模型类（Comment）
        instance: 被删除的评论实例（已从数据库中删除，但对象仍在内存中）
        **kwargs: 其他参数，可能包含：
                 - using: 使用的数据库别名
                 
    触发时机：
        当评论被删除时（无论是管理员删除还是级联删除）
        
    处理逻辑：
        无论被删除的评论是否已审核，都触发词云更新。
        因为如果是已审核的评论被删除，词云数据需要更新；
        如果是未审核的评论被删除，广播也不会造成影响（因为它本来就不在词云中）。
        
    说明：
        当管理员删除一条评论时，该评论的内容不应再出现在词云中，
        所以需要重新计算词云数据并推送更新。
    """
    # 广播词云数据更新（无需检查 is_approved，因为评论已被删除）
    broadcast_comment_wordcloud()
