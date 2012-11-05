# -*- coding: utf-8 -*-
from django.conf.urls import *
from django.contrib import admin
from trailers_shop.apps.callback.views import RequestCallback

from views import handle_ajax

admin.autodiscover()


urlpatterns = patterns('',
    url(r'^$', RequestCallback.as_view(), name='request-callback'),
    url(r'^ajax(?P<url>.*)$', handle_ajax),
)
