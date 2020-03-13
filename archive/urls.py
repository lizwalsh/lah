from django.conf.urls import include, url
from django.urls import reverse

from . import views


app_name = 'archive'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name="index"),
    url(r'^book(\d+)$', views.BookView.as_view(), name="book"),
    url(r'^cal/$', views.show_cal, name="cally"), 
    url(r'^cal/(\d+)/(\d+)/$', views.show_cal, name="cally"), 
    url(r'^guest/$', views.GuestView.as_view(), name="guest")
]
