# -*- coding: utf-8 -*-
from forms import CallbackForm


def forms(request):
    return {'callback_form': CallbackForm()}
