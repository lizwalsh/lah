from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^comics/', include('comics.urls')),
    url(r'^admin/' admin.site.urls),
    url(r'^news/', include('news.urls', namespace="news")),
    url(r'^archive/', include('archive.urls', namespace="archive")),
    url(r'^extras/', include('extras.urls', namespace="photologue")),
]