from django.conf.urls import patterns, include, url
#from django.views.generic import list_detail

from . import views

app_name = 'cast'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name="index"),  
    #url(r'^$', list_detail.object_list, all_models_dict),  
]
