# -*- coding: utf-8 -*-
from django.contrib.sites.models import Site
from django.db import models


class Callback(models.Model):
    site = models.ForeignKey(Site, null=True)
    username = models.CharField(max_length=100, verbose_name=u'Имя')
    comment = models.TextField(u'Комментарий')
    phone_number = models.CharField(max_length=30, verbose_name=u'Телефон',
        blank=True)
    email = models.EmailField(u'Email', blank=True)

    def __unicode__(self):
        return u'callback from  {site}: {phone_number}, {email}, {username}'.format(
            phone_number=self.phone_number,
            email=self.email,
            username=self.username,
            site=self.site.name
        )
