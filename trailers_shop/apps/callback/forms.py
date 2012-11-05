# -*- coding: utf-8 -*-
from django import forms
from django.core.exceptions import ValidationError

from models import Callback


class CallbackForm(forms.ModelForm):
    """
    The form shown when giving callback
    """
    def __init__(self, *args, **kwargs):
        super(CallbackForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({
            'class': 'text',
            'placeholder': u'Как вас зовут?'
        })
        self.fields['comment'].widget.attrs.update({
            'placeholder': u'Введите текст...'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'text',
            'placeholder': u'Укажите электронный адрес для связи'
        })
        self.fields['phone_number'].widget.attrs.update({
            'class': 'text',
            'placeholder': u'Укажите телефон для связи'
        })

    def clean(self):
        cd = super(CallbackForm, self).clean()

        print cd

        if cd.get('email') == '' and cd.get('phone_number') == '':
            self._errors["email_or_phone"] = self.error_class([
                u'Укажите email, либо номер телефона'
            ])

        return cd


    class Meta:
        model = Callback
        exclude = ['site']
