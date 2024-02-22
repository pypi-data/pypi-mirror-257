from django.apps import AppConfig


class DjangoActionLogLogConfig(AppConfig):
    default_auto_field = "django.db.models.AutoField"
    name = "django_action_logger"

    def ready(self):
        from . import signals
