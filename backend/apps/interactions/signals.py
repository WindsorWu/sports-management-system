from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Comment
from .comment_wordcloud import broadcast_comment_wordcloud


@receiver(post_save, sender=Comment)
def handle_comment_save(sender, instance, **kwargs):
    if not instance.is_approved:
        return
    broadcast_comment_wordcloud()


@receiver(post_delete, sender=Comment)
def handle_comment_delete(sender, instance, **kwargs):
    broadcast_comment_wordcloud()
