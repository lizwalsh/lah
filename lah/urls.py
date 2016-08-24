"""lah URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from lah.feeds import RecentUpdates


urlpatterns = [
    url(r'^comics/', include('comics.urls')),
    url(r'^news/', include('news.urls')),
    url(r'^cast/', include('cast.urls')),
    url(r'^about/', include('about.urls')),
    url(r'^archive/', include('archive.urls')),
    url(r'^extras/', include('extras.urls', namespace="photologue")),
    url(r'^admin/', admin.site.urls),
    url(r'^rss/', RecentUpdates() ),
    url(r'^extras/', include('photologue.urls', namespace='photologue')),
    url(r'', include('comics.urls')),
    #url(r'^lifesahowl/', include('twython_django_oauth.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()