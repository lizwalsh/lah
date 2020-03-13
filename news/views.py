from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import datetime
from django.utils import timezone

from .models import NewsItem

# root
class IndexView(generic.ListView):
    model = NewsItem
    template_name = 'news/newslog.html'
    paginate_by = 3
    queryset = NewsItem.objects.filter(published=True).order_by('-date')
    context_object_name = "news"
    

class NewsView(generic.ListView):
    model = NewsItem
    template_name = 'news/newslog.html'
    paginate_by = 3
    queryset = NewsItem.objects.filter(published=True).order_by('-date')
    context_object_name = "news"
    
    """
    def get_context_data(self, **kwargs):
        context = super(NewsView, self).get_context_data(**kwargs)
        thenews = NewsItem.objects.filter(published=True).order_by('-date')
        paginator = Paginator(thenews, self.paginate_by)
        
        page = self.request.GET.get('page')
        try:
            news = paginator.page(page)
        except PageNotAnInteger:
            news = paginator.page(paginator.num_pages)
        except EmptyPage:
            news = paginator.page(paginator.num_pages)
        context['news'] = news
        return context
    
    """
    
class PageView(generic.DetailView):
    model = NewsItem
    template_name = 'news/news.html'
    context_object_name = "news"
    
    def get_queryset(self):
        return NewsItem.objects.filter(published=True, id = self.kwargs['pk'])
    
    