#-*- coding: utf-8 -*-

from django.db.models import signals
from .models import StoreUser
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from stores.models import (
    Cart, Store, Product, Item
)


def add_permissions(sender, instance, created=False, **kwargs):
    if created and instance.is_staff:
        content_types = ContentType.objects.get_for_models(
            Cart, Store, Product, Item
        ).values()
        permissions = Permission.objects.filter(
            content_type__in=content_types)
        instance.user_permissions.add(*permissions)


signals.post_save.connect(add_permissions, sender=StoreUser)
