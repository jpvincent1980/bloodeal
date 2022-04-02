from django.apps import AppConfig


class DealsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'deals'
    verbose_name = "Bons Plans"

    def ready(self):
        import deals.signals
