from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
import datetime

from .models import Archive
from comics.models import Comic


class IndexView(generic.ListView):
    model = Archive
    template_name = 'archive/archive.html'
    context_object_name = 'arc'
    
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        return context
        
    
    def get_queryset(self):
        books = Archive.objects.filter(published=True).order_by('booknum')
        # if we don't have a published book yet, just use the current pages
        if not books:
            clist = Comic.objects.filter(published=True).order_by('date')
            book = Archive(title="Current pages here I go", booknum=0, start_id=clist.earliest(), published=True )
            books = []
            books.append(book)
        return books


    
class BookView(generic.ListView):
    model = Archive
    template_name="archive/archive.html"
    context_object_name = 'arc'
    
    def get_queryset(self):
        self.bookrange = get_object_or_404(Archive, booknum=self.args[0])
        return Comic.objects.filter(published=True, id__range=(self.bookrange.start_id.id, self.bookrange.get_end_comic().id))
        #return self.kwargs
    
class PageView(generic.DetailView):
    model = Archive
    template_name = 'archive/calendar.html'
    
    def get_queryset(self):
        return "foo"
    
class GuestView(generic.DetailView):
    model = Archive
    template_name = 'archive/guest.html'
    
    def get_queryset(self):
        return self.getGuestComics()