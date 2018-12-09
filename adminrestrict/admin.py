"""
adminrestrict app model admin definitions.
"""

__author__ = "Robert Romano (rromano@gmail.com)"
__copyright__ = "Copyright 2014 Robert C. Romano"


from django.contrib import admin
from adminrestrict.models import AllowedIP


class AllowedIPAdmin(admin.ModelAdmin):
    list_display = ('id', 'ip_address', 'description', 'created_by', 'edited_by')
    list_editable = ('ip_address', 'description')
    readonly_fields = ('created_by', 'edited_by')

    def save_model(self, request, instance, form, change):
        user = request.user
        if not change or not instance.created_by:
            instance.created_by = user
        instance.edited_by = user
        return super(AllowedIPAdmin, self).save_model(request, instance, form, change)

admin.site.register(AllowedIP, AllowedIPAdmin)



