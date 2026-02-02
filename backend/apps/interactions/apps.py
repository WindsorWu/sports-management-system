from django.apps import AppConfig


class InteractionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.interactions'
    verbose_name = '互动管理'

    def ready(self):
        # 确保信号处理器在App启动时注册
        import apps.interactions.signals
