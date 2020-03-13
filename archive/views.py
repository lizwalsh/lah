from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
import datetime
from django.utils.safestring import mark_safe
from django.views.generic import View

from .models import Archive, ArchiveCalendar
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
            try:
                clist = Comic.objects.filter(published=True).order_by('date')
                book = Archive(title="", booknum=0, start_id=clist.earliest(), published=True )
            except Comic.DoesNotExist:
                book = Archive(title="", booknum=0, published=True)
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

        
    
class GuestView(generic.DetailView):
    model = Archive
    template_name = 'archive/guest.html'
    
    def get_queryset(self):
        return self.getGuestComics()
    
    
# generic view for calendar
# because I couldn't get a class-based one working
from calendar import monthrange

def named_month(pMonthNumber):
    """
    Return the name of the month, given the month number
    """
    return datetime.date(1900, pMonthNumber, 1).strftime('%B')

def show_cal(request, year=None, month=None):
    """
    Show calendar of events this month
    """
    if year == None:
        # get the current comic as a starting point
        lToday = Comic.objects.filter(published=True).order_by('-date')[0].date
        year = lToday.year
        month = lToday.month

    return calendar(request, year, month)

def calendar(request, pYear, pMonth):
    """
    Show calendar of events for specified month and year
    """
    lYear = int(pYear)
    lMonth = int(pMonth)
    lCalendarFromMonth = datetime.date(lYear, lMonth, 1)
    lCalendarToMonth = datetime.date(lYear, lMonth, monthrange(lYear, lMonth)[1])
    lComics = Comic.objects.filter(published=True, date__gte=lCalendarFromMonth, date__lte=lCalendarToMonth).order_by('date')
    lCalendar = ArchiveCalendar(lComics).formatmonth(lYear, lMonth)
    lPreviousYear = lYear
    lPreviousMonth = lMonth - 1
    if lPreviousMonth == 0:
        lPreviousMonth = 12
        lPreviousYear = lYear - 1
    lNextYear = lYear
    lNextMonth = lMonth + 1
    if lNextMonth == 13:
        lNextMonth = 1
        lNextYear = lYear + 1
    pmn = named_month(lPreviousMonth)
    nmn = named_month(lNextMonth)
        
    # now for something fun:
    # if we have the first or last comics in a collection, we DON'T want to paginate this!
    fComic = lComics[0]
    lComic = lComics.reverse()[0]
    aComic = fComic.get_first()
    bComic = fComic.get_latest()
    
    
    if aComic is None or fComic.id == aComic.id:
        lPreviousYear = 0
        lPreviousMonth = 0
    if bComic is None or lComic.id == bComic.id:
        lNextYear = 0
        lNextMonth = 0
    

    return render(request, 'archive/archive_cal.html', {'Calendar' : mark_safe(lCalendar),
                                                       'Month' : str(lMonth),
                                                       'MonthName' : named_month(lMonth),
                                                       'Year' : str(lYear),
                                                       'PreviousMonth' : str(lPreviousMonth),
                                                       'PreviousMonthName' : pmn,
                                                       'PreviousYear' : str(lPreviousYear),
                                                       'NextMonth' : str(lNextMonth),
                                                       'NextMonthName' : nmn,
                                                       'NextYear' : str(lNextYear),
                                                   })