"""
评论词云模块

本模块实现了基于评论内容的实时词云功能，通过以下步骤生成词云数据：
1. 从数据库中获取最近7天内的已审核评论
2. 对评论内容进行中文分词和词性标注
3. 过滤停用词和无效词汇
4. 统计词频并返回高频词汇
5. 通过 WebSocket 实时推送给前端

主要特性：
- 使用 jieba 分词库进行中文分词和词性标注
- 智能提取名词、形容词+名词、动词+名词的组合
- 支持通过 Django Channels 进行实时广播
"""

import re
from collections import Counter
from datetime import timedelta

import jieba.posseg as pseg
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.apps import apps
from django.utils import timezone

# 停用词集合：过滤掉这些常见但无实际意义的词汇
STOP_WORDS = {
    '的', '是', '在', '我', '有', '就', '这', '那', '们', '和', '与', '及',
    '也', '还', '都', '只', '个', '了', '吗', '呢', '吧', '啊', '哦', '之', '于',
    '为', '你', '你们', '我们', '运动', '赛事'
}

# WebSocket 频道组名称：所有订阅词云更新的客户端都会加入此组
WORDCLOUD_GROUP = 'admin_comment_wordcloud'

# 词云中展示的最大词汇数量
MAX_WORDS = 40

# 分析时获取的最大评论数量（最近的400条）
MAX_COMMENTS = 400


def _clean_text(raw_text: str) -> str:
    """
    清洗文本，只保留中文字符
    
    Args:
        raw_text: 原始文本字符串
        
    Returns:
        str: 只包含中文字符的文本（去除了标点、数字、英文等）
        
    说明：
        使用正则表达式 [\u4e00-\u9fa5] 匹配所有中文字符（Unicode范围）
        去除所有非中文字符，为后续分词做准备
    """
    return re.sub(r'[^\u4e00-\u9fa5]+', '', raw_text or '')


def _get_comment_model():
    """
    动态获取 Comment 模型类
    
    Returns:
        Model: Comment 模型类
        
    说明：
        使用 Django 的 apps.get_model() 方法动态获取模型，
        避免在模块顶部导入可能导致的循环依赖问题
    """
    return apps.get_model('interactions', 'Comment')


def extract_tokens(source: str) -> list[str]:
    """
    从文本中提取有意义的词汇（token）
    
    Args:
        source: 原始评论文本
        
    Returns:
        list[str]: 提取出的词汇列表
        
    处理流程：
        1. 清洗文本，只保留中文字符
        2. 使用 jieba 进行分词和词性标注
        3. 根据词性规则提取有意义的词汇：
           - 名词（n开头的词性）：如"比赛"、"成绩"
           - 形容词+名词组合（a+n）：如"精彩比赛"、"优秀成绩"
           - 动词+名词组合（v+n）：如"参加比赛"、"获得成绩"
        4. 过滤掉长度小于2的词和停用词
        
    词性标记说明（jieba.posseg）：
        - n: 名词（noun）
        - a: 形容词（adjective）
        - v: 动词（verb）
    """
    # 清洗文本，只保留中文字符
    clean_text = _clean_text(source)
    if not clean_text:
        return []

    # 使用 jieba 进行分词和词性标注，结果为 (词, 词性) 的列表
    segments = [(word, flag) for word, flag in pseg.cut(clean_text)]
    tokens = []

    # 遍历所有分词结果，根据词性规则提取token
    for index, (word, flag) in enumerate(segments):
        # 过滤：长度小于2的词或停用词
        if len(word) < 2 or word in STOP_WORDS:
            continue

        # 规则1：提取所有名词
        if flag.startswith('n'):
            tokens.append(word)

        # 规则2：提取"形容词+名词"组合（如"精彩比赛"）
        if flag.startswith('a') and index + 1 < len(segments):
            next_word, next_flag = segments[index + 1]
            if next_flag.startswith('n') and next_word not in STOP_WORDS:
                tokens.append(f"{word}{next_word}")

        # 规则3：提取"动词+名词"组合（如"参加比赛"）
        if flag.startswith('v') and index + 1 < len(segments):
            next_word, next_flag = segments[index + 1]
            if next_flag.startswith('n') and next_word not in STOP_WORDS:
                tokens.append(f"{word}{next_word}")

    return tokens


def collect_wordcloud_data() -> list[dict[str, int]]:
    """
    收集并生成词云数据
    
    Returns:
        list[dict]: 词云数据列表，每项包含 text（词汇）和 weight（权重/频率）
        格式示例：[{"text": "比赛", "weight": 15}, {"text": "成绩", "weight": 10}, ...]
        
    处理流程：
        1. 获取最近7天内的已审核评论（最多400条）
        2. 对每条评论提取有意义的词汇
        3. 统计所有词汇的出现频率
        4. 返回出现频率最高的前40个词汇
        
    说明：
        - 只统计已审核通过的评论（is_approved=True）
        - 时间范围：最近7天
        - 数量限制：最多处理400条评论，返回40个高频词
        - 按评论创建时间倒序排列，优先处理最新评论
    """
    # 动态获取 Comment 模型
    Comment = _get_comment_model()
    
    # 计算时间范围：当前时间往前推7天
    horizon = timezone.now() - timedelta(days=7)
    
    # 查询最近7天内已审核的评论，按创建时间倒序，最多取400条
    comments = Comment.objects.filter(is_approved=True, created_at__gte=horizon).order_by('-created_at')[:MAX_COMMENTS]
    
    # 使用 Counter 统计词频
    counter = Counter()

    # 遍历所有评论，提取词汇并更新计数器
    for comment in comments:
        counter.update(extract_tokens(comment.content))

    # 如果没有统计到任何词汇，返回空列表
    if not counter:
        return []

    # 返回出现频率最高的前 MAX_WORDS 个词汇
    # 格式转换：(词, 频率) -> {"text": 词, "weight": 频率}
    return [
        {"text": word, "weight": frequency}
        for word, frequency in counter.most_common(MAX_WORDS)
    ]


def broadcast_comment_wordcloud() -> None:
    """
    广播词云数据更新到所有已连接的 WebSocket 客户端
    
    说明：
        当评论被创建、更新或删除时，此函数会被信号处理器调用，
        重新计算词云数据并通过 WebSocket 推送给所有订阅的客户端（通常是管理后台）
        
    工作流程：
        1. 获取 Django Channels 的 channel_layer（消息传输层）
        2. 调用 collect_wordcloud_data() 生成最新的词云数据
        3. 通过 group_send 向 WORDCLOUD_GROUP 组内的所有客户端广播消息
        
    消息格式：
        {
            "type": "wordcloud.update",  # 消息类型（会被转换为 wordcloud_update 方法调用）
            "payload": [{"text": "词汇", "weight": 频率}, ...]  # 词云数据
        }
        
    注意：
        - 使用 async_to_sync 将异步的 group_send 转换为同步调用
        - 因为此函数在 Django 信号中被调用，而信号处理器是同步的
        - 消息的 type 字段中的点（.）会被转换为下划线（_）
          即 "wordcloud.update" 会调用 Consumer 的 wordcloud_update 方法
    """
    # 获取 Channels 的消息传输层
    channel_layer = get_channel_layer()
    if not channel_layer:
        # 如果未配置 channel_layer，直接返回（可能在测试环境中）
        return

    # 收集最新的词云数据
    payload = collect_wordcloud_data()
    
    # 向词云频道组广播消息
    # async_to_sync: 将异步函数转换为同步调用
    # group_send: 向指定组内的所有连接发送消息
    async_to_sync(channel_layer.group_send)(
        WORDCLOUD_GROUP,  # 目标频道组
        {
            "type": "wordcloud.update",  # 消息类型（会调用 Consumer 的 wordcloud_update 方法）
            "payload": payload,  # 词云数据负载
        },
    )
