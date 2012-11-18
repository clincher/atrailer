# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import DeleteView, DetailView, FormView, ListView
from shop.models.defaults.cartitem import CartItem
from shop.util.address import assign_address_to_request
from shop.views.checkout import CheckoutSelectionView
from shop_categories.models import Category

from forms import OrderExtraInfoForm, TrailerSearchForm
from signals import payment_instructions_email_notification
from models import Trailer
from trailers_shop.apps.customshop.models import Accessory


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


class TrailerListView(ListView):
    model = Trailer
    template_name = 'snippets/product_list.html'
#    context_object_name = 'product_list'

    def build_filter(self, form):
        qs_filter = {}

        if form.get('cleaned_data'):
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

        else:
            # TODO: вывести страницу "По вашему запросу ничего не найдено" или
            # вывести список всех продуктов
            return {}


    def get_queryset(self):
        trailer_search_form = TrailerSearchForm(self.request.GET or {})
        result = super(TrailerListView, self).get_queryset()
        if trailer_search_form.is_valid():
            result.filter(**self.build_filter(trailer_search_form.cleaned_data))
        return result


class AccessoryListView(ListView):
    model = Accessory
    template_name = 'snippets/acessory_list.html'
#    context_object_name = 'accessory_list'
