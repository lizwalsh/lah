from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

import datetime, requests

# Create your views here.
from .models import AboutItem

class IndexView(generic.ListView):
    context_object_name = 'about_page'
    template_name = 'about/about.html'
    
    def get_queryset(self):
        return AboutItem.objects.all().order_by('id')
    
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        return context