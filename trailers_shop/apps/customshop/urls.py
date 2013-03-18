#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from shop.views.cart import CartDetails, CartItemDetail
from shop.views.checkout import (
    ThankYouView, ShippingBackendRedirectView, PaymentBackendRedirectView)
from shop.views.order import OrderListView, OrderDetailView
from shop.views.product import ProductDetailView

from trailers_shop.apps.customshop.models import Trailer
from trailers_shop.apps.customshop.views import (MyCheckoutSelectionView,
    CartItemDeleteView, TrailerListView, AccessoryListView, AccessoryDetailView,
    CustomCategoryShopListView)


urlpatterns = patterns('',
    # Products
#    url(r'^$',
#        ListView.as_view(
#            model=CustomProduct,
#            template_name="customshop/customproduct_list.html"
#        ),
#        name='product_list'
#    ),
    url(r'^$',
        TrailerListView.as_view(),
        # name='trailer-list'),
#         TemplateView.as_view(template_name="index.html"),
        name='index'
    ),

#    url(r'^catalog/$',
#        ListView.as_view(
#            model=Trailer,
#            template_name="customshop/customproduct_list.html",
#            paginate_by=10
#        ),
#        name='product_list'
#    ),
    url(r'^catalog/(?P<path>[0-9A-Za-z-//]+)/page(?P<page>[0-9]+)/$',
        TrailerListView.as_view(),
        name='product_list'),
    url(r'^catalog/(?P<path>[0-9A-Za-z-//]+)/$',
        TrailerListView.as_view(),
        name='product_list'),
    # url(r'^catalog/(?P<path>[0-9A-Za-z-//]+)/$',
    #     CustomCategoryShopListView.as_view(),
    #     name='product_list'),
    url(r'^catalog/$',
        TrailerListView.as_view(),
        name='product_list'),
    url(r'^catalog/(?P<slug>[0-9A-Za-z-_.//]+)$',
        ProductDetailView.as_view(),
        name='product_detail'
    ),
    # Accessories
    url(r'^accessories/$',
        AccessoryListView.as_view(),
        name='accessory-list'
    ),
    url(r'^accessories/(?P<slug>[0-9A-Za-z-_.//]+)$',
        AccessoryDetailView.as_view(),
        name='accessory_detail'
    ),
    # Payment stuff
    (r'^pay/', include('shop.payment.urls')),
    (r'^ship/', include('shop.shipping.urls')),

    # Cart
    url(r'^cart/delete/$', # DELETE
        CartDetails.as_view(action='delete'),
        name='cart_delete'
    ),
    url(r'^cart/delete/(?P<pk>\d+)/$',
        CartItemDeleteView.as_view(),
        name='cart_delete_single'
    ),
    url('^cart/item/$', # POST
        CartDetails.as_view(action='post'),
        name='cart_item_add'
    ),
    url(r'^cart/$', # GET
        CartDetails.as_view(),
        name='cart'
    ),
    url(r'^cart/update/$',
        CartDetails.as_view(action='put'),
        name='cart_update'
    ),
    # CartItems
    url('^cart/item/(?P<id>[0-9A-Za-z-_.//]+)$',
        CartItemDetail.as_view(),
        name='cart_item'
    ),
    # Checkout
    url(r'^checkout/$',
        MyCheckoutSelectionView.as_view(
           template_name="customshop/selection.html"
        ),
        name='checkout_selection' # First step of the checkout process
    ),
    url(r'^checkout/ship/$',
        ShippingBackendRedirectView.as_view(),
        name='checkout_shipping' # First step of the checkout process
    ),
    url(r'^checkout/pay/$',
        PaymentBackendRedirectView.as_view(),
        name='checkout_payment' # First step of the checkout process
    ),
    url(r'^checkout/thank_you/$',
        ThankYouView.as_view(template_name="customshop/thank_you.html"),
        name='thank_you_for_your_order' # Second step of the checkout process
    ),
    # Orders
    url(r'^orders/$',
        OrderListView.as_view(),
        name='order_list'
    ),
    url(r'^orders/(?P<pk>\d+)/$',
        OrderDetailView.as_view(),
        name='order_detail'
    ),
)
