"""
adminrestrict app model admin definitions.
"""

__author__ = "Robert Romano (rromano@gmail.com)"
__copyright__ = "Copyright 2014 Robert C. Romano"


from django.contrib import admin
from adminrestrict.models import AllowedIP


class AllowedIPAdmin(admin.ModelAdmin):
    list_display = ('id', 'ip_address', 'created_by', 'edited_by')
    readonly_fields = ('created_by', 'edited_by')

admin.site.register(AllowedIP, AllowedIPAdmin)



