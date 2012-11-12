# -*- coding: utf-8 -*-
from forms import TrailerSearchForm

def forms(request):
    return {
        'trailer_search_form': TrailerSearchForm(request.GET or None)
    }
