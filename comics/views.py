# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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
        #context["news"] = NewsItem.objects.filter(published=True).order_by('-date')[:3]
        foo = NewsItem.objects.filter(published=True).order_by('-date')
        paginator = Paginator(foo, 3)
        
        page = self.request.GET.get('page')
        try:
            news = paginator.page(page)
        except PageNotAnInteger:
            news = paginator.page(1)
        except EmptyPage:
            news = paginator.page(paginator.num_pages)
        
        context["news"] = news
        return context
    
    def get_queryset(self):
        comic = Comic.objects.filter(published=True).order_by('-date')
        if comic.exists():
            return comic[0]
        else:
            return None


class PageView(generic.DetailView):
    model = Comic
    template_name = 'comics/comic_stuff.html'
    
    def get_queryset(self):
        return Comic.objects.filter(published=True, date__lte=timezone.now())
    
    