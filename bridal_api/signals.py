# bridal_api/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.apps import apps
from django.conf import settings

# When an Order is created, try to decrement related Dress stock (if those fields exist).
@receiver(post_save, sender=apps.get_model('bridal_api', 'Order'))
def order_post_save(sender, instance, created, **kwargs):
    if not created:
        return
    try:
        # safe-get the dress related object if present
        dress = getattr(instance, 'dress', None)
        if dress is None:
            return

        # if the Dress model has 'stock', decrement it
        if hasattr(dress, 'stock') and dress.stock is not None:
            if dress.stock > 0:
                dress.stock -= 1
                dress.save(update_fields=['stock'])
    except Exception:
        # don't break the request if something goes wrong in the signal
        pass


# When a User is created, if role == 'designer', create a Designer row if not exists
@receiver(post_save, sender=apps.get_model('bridal_api', 'User'))
def user_post_save(sender, instance, created, **kwargs):
    if not created:
        return
    try:
        role = getattr(instance, 'role', None)
        if role == 'designer':
            Designer = apps.get_model('bridal_api', 'Designer')
            # ensure we don't create duplicates
            if not Designer.objects.filter(user=instance).exists():
                Designer.objects.create(user=instance, name=instance.username)
    except Exception:
        pass


# When a Dress is deleted, try to remove its image file from storage
@receiver(post_delete, sender=apps.get_model('bridal_api', 'Product'))
def Product_post_delete(sender, instance, **kwargs):
    try:
        image_field = getattr(instance, 'image', None)
        if image_field:
            # delete file from storage if present
            image_field.delete(save=False)
    except Exception:
        pass
