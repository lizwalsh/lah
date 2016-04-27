from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse

from . import views

app_name = 'archive'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name="index"),
    url(r'^book(\d+)$', views.BookView.as_view(), name="book"),
    url(r'^cal/$', views.PageView.as_view(), name="page"), 
    url(r'^guest/$', views.GuestView.as_view(), name="guest")
]
