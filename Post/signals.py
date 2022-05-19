from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from .models import Blog


@receiver(pre_save, sender=Blog)
def create_slug(sender, created, instance, **kwargs):
    if created and not instance.slug:
        instance.slug = f"{instance.content}-{instance.id}"

