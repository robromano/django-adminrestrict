"""
adminretrict models
"""

__author__ = "Robert Romano (rromano@gmail.com)"
__copyright__ = "Copyright 2014 Robert C. Romano"


from django.db import models
from django.conf import settings

class AllowedIP(models.Model):
    """
    Represents a whitelisted IP address who can access admin pages.
    """
    ip_address = models.CharField(max_length=512)
    description = models.CharField(max_length=512)

    created_by = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name="created_allowed_ip", null=True, editable=False)
    edited_by = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name="edited_allowed_ip", null=True, editable=False)

    def __unicode__(self):
        return u'%s' % self.ip_address







