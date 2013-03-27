# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from models import Callback


@receiver(post_save, sender=Callback)
def callback_notifying(sender, **kwargs):
    from_email = getattr(settings, 'SN_FROM_EMAIL', settings.DEFAULT_FROM_EMAIL)
    owners = getattr(settings, 'SN_OWNERS', settings.ADMINS)
    recipient_list = [owner[1] for owner in owners]
    subject = unicode(kwargs['instance'])
    body = unicode(kwargs['instance'])
    send_mail(subject, body, from_email, recipient_list)
