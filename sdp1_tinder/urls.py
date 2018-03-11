from django.conf.urls import patterns, include, url

from django.contrib import admin

# from djrill import DjrillAdminSite

# admin.site = DjrillAdminSite()
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^grappelli/', include('grappelli.urls')),  # grappelli URLS
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include('app.api.urls')),
    url('^', include('app.urls')),
)

# Debug
from django.conf import settings
if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns(
        '',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT
        }),
    )
    urlpatterns += patterns(
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT
        }),
    )
