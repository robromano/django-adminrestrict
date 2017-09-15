from django.conf.urls import url, include
from django.contrib import admin

try:
    from django.conf.urls import patterns
    urlpatterns = patterns('',
        url(r'^admin/', include(admin.site.urls)),
    )
except ImportError:
    urlpatterns = [
        url(r'^admin/', include(admin.site.urls)),
    ]


