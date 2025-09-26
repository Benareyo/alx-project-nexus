# bridal_api/apps.py
from django.apps import AppConfig

class BridalApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bridal_api'

    def ready(self):
        # import signals to connect them
        import bridal_api.signals  # noqa: F401
