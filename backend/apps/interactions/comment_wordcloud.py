import re
from collections import Counter
from datetime import timedelta

import jieba.posseg as pseg
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.apps import apps
from django.utils import timezone

STOP_WORDS = {
    '的', '是', '在', '我', '有', '就', '这', '那', '们', '和', '与', '及',
    '也', '还', '都', '只', '个', '了', '吗', '呢', '吧', '啊', '哦', '之', '于',
    '为', '你', '你们', '我们', '运动', '赛事'
}
WORDCLOUD_GROUP = 'admin_comment_wordcloud'
MAX_WORDS = 40
MAX_COMMENTS = 400


def _clean_text(raw_text: str) -> str:
    return re.sub(r'[^\u4e00-\u9fa5]+', '', raw_text or '')


def _get_comment_model():
    return apps.get_model('interactions', 'Comment')


def extract_tokens(source: str) -> list[str]:
    clean_text = _clean_text(source)
    if not clean_text:
        return []

    segments = [(word, flag) for word, flag in pseg.cut(clean_text)]
    tokens = []

    for index, (word, flag) in enumerate(segments):
        if len(word) < 2 or word in STOP_WORDS:
            continue

        if flag.startswith('n'):
            tokens.append(word)

        if flag.startswith('a') and index + 1 < len(segments):
            next_word, next_flag = segments[index + 1]
            if next_flag.startswith('n') and next_word not in STOP_WORDS:
                tokens.append(f"{word}{next_word}")

        if flag.startswith('v') and index + 1 < len(segments):
            next_word, next_flag = segments[index + 1]
            if next_flag.startswith('n') and next_word not in STOP_WORDS:
                tokens.append(f"{word}{next_word}")

    return tokens


def collect_wordcloud_data() -> list[dict[str, int]]:
    Comment = _get_comment_model()
    horizon = timezone.now() - timedelta(days=7)
    comments = Comment.objects.filter(is_approved=True, created_at__gte=horizon).order_by('-created_at')[:MAX_COMMENTS]
    counter = Counter()

    for comment in comments:
        counter.update(extract_tokens(comment.content))

    if not counter:
        return []

    return [
        {"text": word, "weight": frequency}
        for word, frequency in counter.most_common(MAX_WORDS)
    ]


def broadcast_comment_wordcloud() -> None:
    channel_layer = get_channel_layer()
    if not channel_layer:
        return

    payload = collect_wordcloud_data()
    async_to_sync(channel_layer.group_send)(
        WORDCLOUD_GROUP,
        {
            "type": "wordcloud.update",
            "payload": payload,
        },
    )
