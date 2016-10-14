from django.conf.urls import include, url
#from django.views.generic import list_detail

from . import views

app_name = 'about'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name="index"),   
]
