from django.apps import AppConfig


class BluraysConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blurays'

    def ready(self):
        import blurays.signals
