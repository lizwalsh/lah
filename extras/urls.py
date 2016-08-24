from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse

from . import views

app_name = 'extras'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),  
    url(r'^photo/(?P<slug>[\-\d\w]+)/$', views.PhotoDetailView.as_view(), name='pl-photo'),
    url(r'^fanart/$', views.FanartView.as_view(), name="fanart"),
    #url(r'^downloads/$', views.DownloadView.as_view(), name="downloads"),
    url(r'^info/$', views.InterestView.as_view(), name="interesting"),
    url(r'^contributions/$', views.ContribView.as_view(), name="mycontrib"),
    url(r'^media/$', views.MediaView.as_view(), name="media"),
    url(r'^fanworks/$', views.FanworksView.as_view(), name="fanworks"),
    # 
]
