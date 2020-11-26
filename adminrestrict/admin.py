"""
adminrestrict app model admin definitions.
"""

__author__ = "Robert Romano"
__copyright__ = "Copyright 2021 Robert C. Romano"


from django.contrib import admin
from adminrestrict.models import AllowedIP

import adminrestrict.signals

class AllowedIPAdmin(admin.ModelAdmin):
    list_display = ('id', 'ip_address')

admin.site.register(AllowedIP, AllowedIPAdmin)



