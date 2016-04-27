from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^comics/', include('comics.urls')),
    url(r'^admin/' admin.site.urls),
    url(r'^news/', include('news.urls')),
]