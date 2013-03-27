from django.conf import settings
from django.conf.urls import patterns, url, include
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
#    (r'^admin/filebrowser/', include('filebrowser.sites.urls')),
    (r'^tinymce/', include('tinymce.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^tinymce/', include('tinymce.urls')),
   (r'^grappelli/', include('grappelli.urls')),
#    url(r'^', include('apps.articles.urls')),
#    (r'^cart/', include('shop_simplevariations.urls')),
    (r'^', include('atrailer.apps.customshop.urls')),
#    url(r'^catalog/', include('shop_categories.urls')),
    (r'^callback/', include('atrailer.apps.callback.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^static/(?P<path>.*)$', 'serve'),
    )
    urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^media/(?P<path>.*)$', 'serve'),
    )
