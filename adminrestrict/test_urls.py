from django.contrib import admin
from django import VERSION

if VERSION[0] < 2:
    from django.conf.urls import url, include
    try:
        from django.conf.urls import patterns
        urlpatterns = patterns('',
            url(r'^admin/', include(admin.site.urls)),
        )
    except ImportError:
        urlpatterns = [
            url(r'^admin/', include(admin.site.urls))
        ]
else:
    if VERSION[0] >= 4:
        from django.urls import include, re_path
        urlpatterns = [
            re_path('admin/', admin.site.urls)
        ]        
    else:
        from django.conf.urls import url, include
        from django.urls import path
        urlpatterns = [
            path('admin/', admin.site.urls)
        ]
