# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.views.generic import DeleteView, DetailView, FormView, ListView
from shop.models.defaults.cartitem import CartItem
from shop.util.address import assign_address_to_request
from shop.views.checkout import CheckoutSelectionView
from shop.views import ShopListView
from shop.models import CartItem
from shop_categories.models import Category

from forms import OrderExtraInfoForm, TrailerSearchForm
from signals import payment_instructions_email_notification
from models import Trailer, Accessory


class MyCheckoutSelectionView(CheckoutSelectionView):

    def post(self, *args, **kwargs):
        """ Called when view is POSTed """
        shipping_form = self.get_shipping_address_form()

        if shipping_form.is_valid():

            # Add the address to the order
            shipping_address = shipping_form.save()
            order = self.create_order_object_from_cart()

            self.save_addresses_to_order(order, shipping_address,
                                         shipping_address)

            assign_address_to_request(self.request, shipping_address)
            assign_address_to_request(self.request, shipping_address,
                                      shipping=False)

            billingshipping_form = (
                self.get_billing_and_shipping_selection_form())
            if billingshipping_form.is_valid():
                self.request.session['payment_backend'] = (
                    billingshipping_form.cleaned_data['payment_method'])
                self.request.session['shipping_backend'] = (
                    billingshipping_form.cleaned_data['shipping_method'])
                orderextrainfo_form = OrderExtraInfoForm(self.request.POST)
                if orderextrainfo_form.is_valid():
                    orderextrainfo = orderextrainfo_form.save(commit=False)
                    orderextrainfo.order = order
                    orderextrainfo.save()
                payment_instructions_email_notification(
                    order=order,
                    address=shipping_address,
                    request=self.request
                )
                return HttpResponseRedirect(reverse('checkout_shipping'))

        return self.get(self, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(MyCheckoutSelectionView, self).get_context_data(**kwargs)
        orderextrainfo_form = OrderExtraInfoForm()
        ctx.update({'orderextrainfo_form': orderextrainfo_form})
        return ctx


class CartItemDeleteView(DeleteView):
    model = CartItem

    success_url = '/cart/'

    def get(self, request, *args, **kwargs):
        raise Http404('not found')


class CustomCategoryShopListView(ShopListView):
    paginate_by = 10
    model = Trailer
    template_name = 'customshop/product_list.html'
    context_object_name = 'product_list'
    category = None

    def get_queryset(self):
        try:
            self.category = Category.objects.get(path=self.kwargs['path'])
        except (Category.DoesNotExist, KeyError):
            return super(CustomCategoryShopListView, self).get_queryset()
        categories = [self.category.id] + list(
            self.category.children.values_list('id', flat=True))
        return super(CustomCategoryShopListView, self).get_queryset().filter(
            category__in=categories).distinct()

    def get_context_data(self, **kwargs):
        if self.category:
            kwargs['category'] = self.category
        return super(CustomCategoryShopListView,
                     self).get_context_data(**kwargs)


class TrailerListView(CustomCategoryShopListView):
    model = Trailer

    def build_filter(self, form):
        qs_filter = {}
        data = form.cleaned_data
        #length and capacity is a float and int, so it complex
        if 0 < len(data['length']) < len(form.LENGTH_CHOICES):
            if form.SHORT in data['length']:
                qs_filter['length__lte'] = 3
            if form.LONG in data['length']:
                qs_filter['length__gte'] = 3
        if (data['capacity']
                and len(data['capacity']) < len(form.CAPACITY_CHOICES)):
            if form.SMALL in data['capacity']:
                qs_filter['capacity__lte'] = 8
            if form.BIG in data['capacity']:
                qs_filter['capacity__gte'] = 8
        if 0 < len(data['availability_of_brakes']) < len(form.BRAKES_CHOICES):
            if form.WITH_BRAKES in data['availability_of_brakes']:
                qs_filter['availability_of_brakes'] = True
            if form.NO_BRAKES in data['availability_of_brakes']:
                qs_filter['availability_of_brakes'] = False
        if 0 < len(data['number_axis']) < len(Trailer.NUMBER_AXIS_CHOICES):
            qs_filter['number_axis__in'] = data['number_axis']
        if (data['suspension']
                and len(data['suspension']) < len(Trailer.SUSPENSION_CHOICES)):
            qs_filter['suspension__in'] = data['suspension']
        return qs_filter

    def get_queryset(self):
        trailer_search_form = TrailerSearchForm(self.request.GET or {})
        qs = super(TrailerListView, self).get_queryset()
        if trailer_search_form.is_valid():
            return qs.filter(**self.build_filter(trailer_search_form))
        return qs


class AccessoryListView(CustomCategoryShopListView):
    model = Accessory
    template_name = 'customshop/acessory_list.html'
#    context_object_name = 'accessory_list'


class AccessoryDetailView(DetailView):
    model = Accessory
    template_name = 'shop/accessory_detail.html'
