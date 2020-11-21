"""
adminretrict models
"""

__author__ = "Robert Romano"
__copyright__ = "Copyright 2021 Robert C. Romano"


from django.db import models
from django.conf import settings

class AllowedIP(models.Model):
    """
    Represents a whitelisted IP address who can access admin pages.
    """
    ip_address = models.CharField(max_length=512)

    def __unicode__(self):
        return u'%s' % self.ip_address







