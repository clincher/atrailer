from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import generic
from shop.admin.orderadmin import OrderAdmin
from shop.models import Order
from shop_categories.models import Category
from shop_categories.admin import ProductCategoryAdmin


from models import Trailer, Accessory, ProductImage

#class ProductImageAdmin(admin.TabularInline):
#    """
#    this class is for set up product admin image classes through one point
#    """
#    extra = 1


class NameSlug(admin.ModelAdmin):
    """
    this class is for set up all product admin classes through one point
    """
    prepopulated_fields = {"slug": ("name",)}


class ProductImageInline(generic.GenericTabularInline):
    model = ProductImage
    extra = 1


class TrailerAdmin(NameSlug):
    inlines = [ProductImageInline,]
    class Media:
        js = ('tiny_mce/tiny_mce.js',
              'filebrowser/js/TinyMCEAdmin.js',)



class AccessoryAdmin(NameSlug):
    inlines = [ProductImageInline,]
    class Media:
        js = ('tiny_mce/tiny_mce.js',
              'filebrowser/js/TinyMCEAdmin.js',)


class MyOrderAdmin(OrderAdmin):
    fieldsets = (
            (None, {'fields': ('user', 'status', 'order_total',
                'order_subtotal', 'created', 'modified')}),
            (_('Shipping'), {
                'fields': ('shipping_address_text',),
                }),
            )


admin.site.register(Category, ProductCategoryAdmin)
admin.site.register(Trailer, TrailerAdmin)
admin.site.register(Accessory, AccessoryAdmin)
admin.site.unregister(Order)

#ORDER_MODEL = getattr(settings, 'SHOP_ORDER_MODEL', None)
#if not ORDER_MODEL:
admin.site.register(Order, MyOrderAdmin)
