from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from crum import get_current_request

from .models import DjangoActionLogEntry


@receiver(post_save)
def log_save(sender, instance, created, raw, using, update_fields, **kwargs):
    if sender is DjangoActionLogEntry:
        return
    user = None
    request = get_current_request()
    if request:
        user = request.user
    if created:
        DjangoActionLogEntry.objects.add_something(user, instance)
    else:
        if update_fields:
            update_fields = list(update_fields)
        DjangoActionLogEntry.objects.change_something(user, instance, update_fields)


@receiver(post_delete)
def log_delete(sender, instance, using, origin, **kwargs):
    if sender is DjangoActionLogEntry:
        return
    user = None
    request = get_current_request()
    if request:
        user = request.user
    DjangoActionLogEntry.objects.delete_something(user, instance)
