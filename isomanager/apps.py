from django.apps import AppConfig


class IsomanagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'isomanager'

    def ready(self):
        from . import signals  # noqa
