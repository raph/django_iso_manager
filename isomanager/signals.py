from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Datastore


@receiver(post_save, sender=Datastore)
def datastore_post_save(sender, instance, created, raw=False, **kwargs):
    """
    post save signal in order to scan iso files for each new created datastore
    """
    if created:
        instance.scan()
