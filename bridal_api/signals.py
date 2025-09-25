# bridal_api/signals.py
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import Designer

User = get_user_model()

@receiver(post_save, sender=User)
def create_designer_profile(sender, instance, created, **kwargs):
    """
    When a user is created with role 'designer' create a Designer profile automatically.
    Also if a user is updated and role flips to 'designer' create profile if not exists.
    """
    try:
        if getattr(instance, "role", "") == "designer":
            Designer.objects.get_or_create(user=instance, defaults={"name": instance.username, "email": instance.email})
    except Exception:
        # keep signal resilient in dev
        pass
