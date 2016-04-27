from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse

from . import views

app_name = 'comics'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),  
    url(r'^(?P<pk>[0-9]+)/(?P<slug>[\w\d-]+)/$', views.PageView.as_view(), name="page"), 
    # 
]
