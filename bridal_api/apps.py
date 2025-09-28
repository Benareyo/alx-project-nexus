# bridal_api/apps.py
from django.apps import AppConfig
#from django.contrib.auth.models import User

class BridalApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bridal_api'

    def ready(self):
        # import signals to connect them
        import bridal_api.signals  # noqa: F401
# bridal_api/apps.py
from django.apps import AppConfig
from django.conf import settings
from django.core.management import call_command
import os

class BridalApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bridal_api'

    def ready(self):
        import bridal_api.signals  # noqa: F401

        # Only run this when the app is fully loaded and migrations are applied
        if os.environ.get("RUN_MAIN") == "true":
            from django.contrib.auth import get_user_model
            User = get_user_model()

            try:
                # Check if any superuser exists
                if not User.objects.filter(is_superuser=True).exists():
                    # Load the fixture
                    fixture_path = os.path.join(settings.BASE_DIR, 'bridal_api', 'fixtures', 'initial_superuser.json')
                    call_command('loaddata', fixture_path)
                    print("✅ Initial superuser created from fixture.")
            except Exception as e:
                # Just print the error; this avoids breaking startup if DB not ready
                print(f"⚠️ Could not create superuser automatically: {e}")
