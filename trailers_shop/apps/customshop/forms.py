# -*- coding: utf-8 -*-
from itertools import chain

from django.utils.html import conditional_escape
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django import forms
from django.forms.widgets import CheckboxSelectMultiple, CheckboxInput
from shop.models import OrderExtraInfo

from models import Trailer


class OrderExtraInfoForm(forms.ModelForm):
    class Meta:
        model = OrderExtraInfo
        fields = ('text',)


class CustomCheckboxSelectMultiple(CheckboxSelectMultiple):
    def render(self, name, value, attrs=None, choices=()):
        if value is None: value = []
        has_id = attrs and 'id' in attrs
        final_attrs = self.build_attrs(attrs, name=name)
        output = [u'']
        # Normalize to strings
        str_values = set([force_unicode(v) for v in value])
        for i, (option_value, option_label) in enumerate(
        chain(self.choices, choices)):
            # If an ID attribute was given, add a numeric index as a suffix,
            # so that the checkboxes don't all have the same ID attribute.
            if has_id:
                final_attrs = dict(final_attrs, id='%s_%s' % (attrs['id'], i))
                label_for = u' for="%s"' % final_attrs['id']
            else:
                label_for = ''

            cb = CheckboxInput(final_attrs,
                check_test=lambda value: value in str_values)
            option_value = force_unicode(option_value)
            rendered_cb = cb.render(name, option_value)
            option_label = conditional_escape(force_unicode(option_label))
            output.append(u'<label%s>%s %s</label>' % (
                label_for, rendered_cb, option_label))
        return mark_safe(u'\n'.join(output))

class TrailerSearchForm(forms.Form):
    SHORT = 1
    LONG = 2
    LENGTH_CHOICES = (
        (SHORT, 'от 1,5 до 3 метров'),
        (LONG, 'от 3 до 6 метров'),
    )

    SMALL = 1
    BIG = 2
    CAPACITY_CHOICES = (
        (SMALL, 'до 8 тонн'),
        (BIG, 'от 8 тонн'),
    )

    NO_BRAKES = 0
    WITH_BRAKES = 1
    BRAKES_CHOICES = (
        (NO_BRAKES, 'без тормозов'),
        (WITH_BRAKES, 'с тормозами'),
    )

    number_axis = forms.MultipleChoiceField(Trailer.NUMBER_AXIS_CHOICES, False,
        CustomCheckboxSelectMultiple, 'Количество осей')
    suspension = forms.MultipleChoiceField(Trailer.SUSPENSION_CHOICES, False,
        CustomCheckboxSelectMultiple, 'Подвеска')
    length = forms.MultipleChoiceField(LENGTH_CHOICES, False,
        CustomCheckboxSelectMultiple, 'Длина платформы')
    capacity = forms.MultipleChoiceField(CAPACITY_CHOICES, False,
        CustomCheckboxSelectMultiple, 'Грузоподъемность')
    availability_of_brakes = forms.MultipleChoiceField(BRAKES_CHOICES, False,
        CustomCheckboxSelectMultiple, 'Наличие тормозов')
