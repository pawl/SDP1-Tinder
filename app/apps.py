from django.apps import AppConfig


class DefaultAppConfig(AppConfig):
    name = 'app'

    def ready(self):
        import app.signals
