from django.apps import AppConfig
from django.core.signals import setting_changed


class AppConfig(AppConfig):
    name = 'app'

    def ready(self):
        import app.signals
