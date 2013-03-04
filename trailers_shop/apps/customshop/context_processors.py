# -*- coding: utf-8 -*-
from forms import TrailerSearchForm
from shop_categories.models import Category


def forms(request):
    return {'trailer_search_form': TrailerSearchForm(request.GET or None)}


def categories(request):
    return {'categories': Category.objects.all()}
