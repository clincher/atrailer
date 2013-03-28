from django.conf import settings
from django.conf.urls import patterns, url, include
from django.contrib import admin
from filebrowser.sites import site

admin.autodiscover()

urlpatterns = patterns('',
#    (r'^admin/filebrowser/', include('filebrowser.sites.urls')),
    (r'^tinymce/', include('tinymce.urls')),
    url(r'^admin/filebrowser/', include(site.urls)),
    (r'^admin/', include(admin.site.urls)),
    (r'^tinymce/', include('tinymce.urls')),
   (r'^grappelli/', include('grappelli.urls')),
    (r'^', include('atrailer.apps.customshop.urls')),
    (r'^callback/', include('atrailer.apps.callback.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^static/(?P<path>.*)$', 'serve'),
    )
    urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^media/(?P<path>.*)$', 'serve'),
    )
