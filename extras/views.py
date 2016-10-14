from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
import datetime
from .models import Fanart, InfoType
from photologue.models import Gallery, Photo

from django.utils import timezone

class IndexView(generic.ListView):
    model = Gallery
    template_name = 'extras/extras.html'
    context_object_name = 'extras'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        
        context["fanart"] = Gallery.objects.get(title="Fanart")
        context["media"] = InfoType.objects.filter(type='media')
        context["interesting"] = InfoType.objects.filter(type='interesting')
        context["mycontrib"] = InfoType.objects.filter(type='mycontrib')
        context["fanworks"] = InfoType.objects.filter(type='fanworks')
        return context
    

class FanartView(generic.ListView):
    model = Gallery
    template_name = 'extras/extras_fanworks.html'
    queryset = Gallery.objects.on_site().is_public()
    context_object_name = 'fangallery'
    
    def get_context_data(self, **kwargs):
        context = super(generic.ListView, self).get_context_data(**kwargs)
        context["fanart"] = Gallery.objects.get(title="Fanart")
        context["fanworks"] = InfoType.objects.filter(type="fanworks")
        return context
    
class DownloadView(generic.ListView):
    model = Gallery
    template_name = "extras/extras.html"
    context_object_name = 'downloads'
    
class PhotoDetailView(generic.DetailView):
    model = Photo
    template_name = 'extras/extras_fanart_detail.html'
    queryset = Photo.objects.on_site().is_public()  
    context_object_name='fanpiece'
    
    def get_context_data(self, **kwargs):
        context = super(PhotoDetailView, self).get_context_data(**kwargs)
        context["attrib"] = Fanart.objects.get(photo=self.object)
        return context

class InterestView(generic.ListView):
    model = InfoType
    template_name = 'extras/extras_interesting.html'
    queryset = InfoType.objects.filter(type='interesting')
    context_object_name='interesting'
    
class MediaView(generic.ListView):
    model = InfoType
    template_name = 'extras/extras_media.html'
    queryset = InfoType.objects.filter(type='media')
    context_object_name='media'
    
class ContribView(generic.ListView):
    model = InfoType
    template_name = 'extras/extras_contributions.html'
    queryset = InfoType.objects.filter(type='mycontrib')
    context_object_name='mycontrib'
    