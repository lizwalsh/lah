from django.conf.urls import include, url

from . import views

app_name = 'news'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name="index"),  
    #url(r'^page/(?P<pk>[0-9]+)/$', views.NewsView.as_view(), name="newslog" ),
    url(r'^(?P<pk>[0-9]+)/(?P<slug>[\w\d-]+)/$', views.PageView.as_view(), name="page"), 
]
