from django.db import models
from django.conf import settings

from calendar import HTMLCalendar
from datetime import date
from itertools import groupby
from django.utils.html import conditional_escape as esc

from comics.models import Comic, GuestComic

class Archive(models.Model):
    start_id = models.ForeignKey(Comic, related_name='Starting comic+')
    booknum = models.IntegerField('Book number', default=1)
    title = models.CharField(max_length=200)
    published = models.BooleanField('is published?', default=False)
    
    def __str__(self):
        return "Book " + str(self.booknum) + ": " + str(self.title)
    
    def save(self, *args, **kwargs):
        super(Archive, self).save(*args, **kwargs)
        
    # gets all the relevant comics for an archive
    # HOLY CRAP this is easier to handle!
    def get_comics(self):
        return Comic.objects.filter(published=True, date__range=(self.start_id.date, self.get_end_comic().date)).order_by('date')
    
    # determine if archive is latest archive
    def isLatest(self):
        try:
            latest = Archive.objects.filter(published=True).order_by('-booknum')[0]
            val = ( (self.booknum == latest.booknum) and (self.id == latest.id) )
        except Archive.DoesNotExist:
            val = True
        except IndexError:
            val = True
        return val
    
    # get the end comic for a range
    def get_end_comic(self):
        if self.isLatest():
            return Comic.objects.filter(published=True, date__gte=self.start_id.date).order_by('-date')[0]
        else:
            nextbook = Archive.objects.get(booknum=(self.booknum + 1))
            return nextbook.start_id.get_prev()
        
    # get all guest comics
    def getGuestComics(self):
        return Comic.objects.filter(published=True, guest=True)
    
class ArchiveCalendar(HTMLCalendar):
    def __init__(self, comics):
        super(ArchiveCalendar, self).__init__()
        self.comics = self.group_by_day(comics)
        
    def formatday(self, day, weekday):
        if day != 0:
            cssclass = self.cssclasses[weekday]
            if date.today() == date(self.year, self.month, day):
                cssclass += ' today'
            if day in self.comics:
                cssclass += ' filled'
                body = []
                for comic in self.comics[day]:
                    body.append('<a href="%s">' % comic.get_url() )
                    body.append(esc(comic))
                    body.append('</a>')
                body.append('</ul>')
                return self.day_cell(cssclass, '%d %s' % (day, ''.join(body) ) )
            return self.day_cell(cssclass, day)
        return self.day_cell('noday', '&nbsp;')
    
    def formatmonth(self, year, month):
        self.year, self.month = year, month
        return super(ArchiveCalendar, self).formatmonth(year, month)

    def group_by_day(self, comics):
        field = lambda comic: comic.date.day
        return dict(
            [(day, list(items)) for day, items in groupby(comics, field)]
        )

    def day_cell(self, cssclass, body):
        return '<td class="%s">%s</td>' % (cssclass, body)
    
    