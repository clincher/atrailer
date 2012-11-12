# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from mptt.fields import TreeForeignKey
from shop.models.productmodel import Product
from shop.order_signals import completed

from trailers_shop.apps.common.models import ObjectMixin, upload_to
from trailers_shop.apps.customshop.signals import confirmed_email_notification


class ProductImage(models.Model):
    alt = models.CharField(max_length=200,
        verbose_name=u'Описание изображения',
        help_text=u'не больше 200 символов и желательно не больше 16 слов')
    src = models.ImageField(upload_to=upload_to, verbose_name=u'Изборажение')
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()

    class Meta:
        ordering = ('id',)

    def __unicode__(self):
        return u'{alt}"'.format(alt=self.alt)

#    def url(self):
#        return '{MEDIA_URL}{src}'.format(
#            MEDIA_URL=settings.MEDIA_URL, src=self.src)


class BaseProduct(Product, ObjectMixin):
    long_text = models.TextField(u'Описание для страницы товара')
    category = TreeForeignKey('shop_categories.Category')

    images = generic.GenericRelation(ProductImage)

    class Meta:
        abstract = True

    def logo(self):
        try:
            return self.images.all()[0]
        except IndexError:
            return None

    @models.permalink
    def get_absolute_url(self):
        return 'product_detail', (), {'slug':self.slug}

#    def save(self, *args, **kwargs):
#        super(BaseProduct, self).save(*args, **kwargs)
#        self.additional_categories.add(self.main_category)


class Trailer(BaseProduct):
    """Master data: info about product"""
    UNIAXIAL = 1
    BIAXIAL = 2
    NUMBER_AXIS_CHOICES = (
        (UNIAXIAL, 'одноосный'),
        (BIAXIAL, 'двухосный')
    )

    SUSPENSION_CHOICES = (
        (1, 'Резино-жгутовая'),
        (2, 'Рессорная')
    )


    length = models.FloatField('Длина платформы', null=False, blank=False)
    number_axis = models.PositiveSmallIntegerField('Количество осей',
        choices=NUMBER_AXIS_CHOICES, null=False, blank=False)
    suspension = models.PositiveSmallIntegerField('Подвеска',
        choices=SUSPENSION_CHOICES, null=False, blank=False)
    capacity = models.FloatField('Грузоподъемность', null=False, blank=False)
    availability_of_brakes = models.BooleanField('наличие тормозов')

    similar = models.ManyToManyField('self', verbose_name='похожие',
        null=True, blank=True)

    class Meta:
        verbose_name = u'Прицеп'
        verbose_name_plural = u'Прицепы'

    def __unicode__(self):
        return u'{0}'.format(self.name)


class Accessory(BaseProduct):
    """Master data: info about product"""
    recent = models.ManyToManyField(Trailer, verbose_name='подходит к',
        related_name='accessories', null=True, blank=True)

    class Meta:
        verbose_name = u'Аксессуар'
        verbose_name_plural = u'Аксессуары'

    def __unicode__(self):
        return u'{0}'.format(self.name)


completed.connect(confirmed_email_notification)
