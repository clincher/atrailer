# -*- coding: utf-8 -*-
import json

from django.contrib.sites.models import Site
from django.http import HttpResponse
from django.utils.encoding import force_unicode
from django.views.generic.base import TemplateView
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url

from forms import CallbackForm


def sanitize(errors):
    return dict((str(k), map(force_unicode, v)) for k, v in errors.iteritems())


def handle_ajax(request, url):
    if not request.POST:
        return HttpResponse(json.dumps({'error':'no post recieved'}))
    else:
        form = CallbackForm(request.POST)
        if form.is_valid():
            callback = form.save(commit=False)
            callback.site = Site.objects.get_current()
            callback.save()
            return HttpResponse(json.dumps({}))
        else:
            result = dict()
            result['status'] = 0
            result['errors'] = form.errors

            result['new_cptch_key'] = CaptchaStore.generate_key()
            result['new_cptch_image'] = captcha_image_url(
                result['new_cptch_key'])

            return HttpResponse(json.dumps(result))


class RequestCallback(TemplateView):
    template_name = 'callback/callback.html'

    def get_context_data(self, **kwargs):
        ctx = super(RequestCallback, self).get_context_data(**kwargs)

        ctx.update({
            'form': CallbackForm()
        })

        return ctx
