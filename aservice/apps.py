from django.apps import AppConfig


class AserviceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'aservice'

    def ready(self):
        import aservice.signals
