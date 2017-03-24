from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic

import datetime, requests

# Create your views here.
from .models import Intro, CastEntry

class IndexView(generic.ListView):
    context_object_name = 'cast_page'
    model = CastEntry
    template_name = 'cast/cast.html'
    
    def get_queryset(self):
        return CastEntry.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        try:
            context["intro"] = Intro.objects.all().first()
        except Intro.DoesNotExist:
            context["intro"] = None
        return context

    

