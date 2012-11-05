from django.conf import settings
from django.conf.urls.defaults import patterns, url, include
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/filebrowser/', include('filebrowser.urls')),
    (r'^tinymce/', include('tinymce.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^tinymce/', include('tinymce.urls')),
#    (r'^feedback/', include('feedback.urls')),
#    url(r'^', include('apps.articles.urls')),
#    (r'^cart/', include('shop_simplevariations.urls')),
    url(r'^catalog/', include('shop_categories.urls')),
    (r'^', include('trailers_shop.apps.customshop.urls')),
    (r'^callback/', include('trailers_shop.apps.callback.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^static/(?P<path>.*)$', 'serve'),
    )
    urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^media/(?P<path>.*)$', 'serve'),
    )
