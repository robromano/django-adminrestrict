"""
adminrestrict signals
"""

__author__ = "Robert Romano"
__copyright__ = "Copyright 2020 Robert C. Romano"

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from adminrestrict.models import AllowedIP
from adminrestrict.middleware import AdminPagesRestrictMiddleware

@receiver(post_save, sender=AllowedIP)
def allowed_ip_saved(sender, instance, created, **kwargs):
    AdminPagesRestrictMiddleware._invalidate_cache = True


@receiver(post_delete, sender=AllowedIP)
def allowed_ip_deleted(sender, instance, using, **kwargs):
    AdminPagesRestrictMiddleware._invalidate_cache = True

