# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
import datetime

from django.utils import timezone

from .models import Comic
from news.models import NewsItem


class IndexView(generic.ListView):
    model = Comic
    template_name = 'index.html'
    context_object_name = 'comic'
    
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context["news"] = NewsItem.objects.filter(published=True).order_by('-date')[:3]
        return context
    
    def get_queryset(self):
        return Comic.objects.filter(published=True).order_by('-date')[0]

class PageView(generic.DetailView):
    model = Comic
    template_name = 'comics/comic_stuff.html'
    
    def get_queryset(self):
        return Comic.objects.filter(published=True, date__lte=timezone.now())
    
    