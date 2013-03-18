# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.template.defaultfilters import yesno
from mptt.fields import TreeForeignKey
from shop.models.productmodel import Product
from shop.order_signals import completed

from trailers_shop.apps.common.models import ObjectMixin, upload_to
from trailers_shop.apps.customshop.signals import confirmed_email_notification


class ProductImage(models.Model):
    alt = models.CharField(
        max_length=200, verbose_name=u'Описание изображения',
        help_text=u'не больше 200 символов и желательно не больше 16 слов')
    src = models.ImageField(u'Изборажение', upload_to=upload_to)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()

    class Meta:
        db_table = 'shop_productimage'
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
        return 'product_detail', (), {'slug': self.slug}

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

    length = models.FloatField(
        u'Длина платформы', null=False, blank=False, help_text=u'м')
    number_axis = models.PositiveSmallIntegerField(
        u'Количество осей', choices=NUMBER_AXIS_CHOICES, null=False, blank=False)
    suspension = models.PositiveSmallIntegerField(
        u'Подвеска', choices=SUSPENSION_CHOICES, null=False, blank=False)
    capacity = models.FloatField(
        u'Грузоподъемность', null=False, blank=False, help_text=u'тонн')
    availability_of_brakes = models.BooleanField(u'Наличие тормозов')

    similar = models.ManyToManyField(
        'self', verbose_name=u'похожие', null=True, blank=True)

    class Meta:
        verbose_name = u'Прицеп'
        verbose_name_plural = u'Прицепы'

    def __unicode__(self):
        return u'{0}'.format(self.name)

    def get_property(self, format, field_name):
        field = self._meta.get_field(field_name)
        args = [field.verbose_name]

        if field.choices:
            args.append(getattr(self, 'get_' + field_name + '_display')())
        elif issubclass(field.__class__, models.BooleanField):
            args.append(yesno(getattr(self, field_name), u'есть,нету'))
        else:
            args.append(getattr(self, field_name))
        if field.help_text:
            args.append(field.help_text)
        return format.format(*args)

    def get_property_list(self):
        return [self.get_property(*args) for args in
                (u'- {0}: {1:g} {2}', 'length'),
                (u'- {0}: {1}', 'number_axis'),
                (u'- {0}: {1}', 'suspension'),
                (u'- {0}: {1:g} {2}', 'capacity'),
                (u'- {0}: {1}', 'availability_of_brakes')
        ]


class Accessory(BaseProduct):
    """Master data: info about product"""
    recent = models.ManyToManyField(
        Trailer, verbose_name='подходит к', related_name='accessories',
        null=True, blank=True)

    class Meta:
        verbose_name, verbose_name_plural = u'Аксессуар', u'Аксессуары'

    def __unicode__(self):
        return u'{0}'.format(self.name)


completed.connect(confirmed_email_notification)
