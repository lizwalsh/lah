from django.db import models
from django.conf import settings

from comics.models import Comic

class Archive(models.Model):
    start_id = models.ForeignKey(Comic, related_name='Starting comic+')
    #end_id = models.ForeignKey(Comic, related_name='Ending comic+')
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
    
    """
    # whenever a book gets a new end id, make sure the next book to it gets its corresponding ID redone
    def set_endpage(self):
        try:
            nextbook = Archive.objects.get(booknum=(self.booknum + 1))
            new_startpage = self.end_id.get_next()
            setattr(nextbook, 'start_id', new_endpage)
            nextbook.save()
        except Archive.DoesNotExist:
            return None
    
        
    # whenever a book gets a new start id, make sure the previous book to it gets its corresponding ID redone
    def set_startpage(self):
        try:
            prevbook = Archive.objects.get(booknum=(self.booknum - 1))
            new_endpage = self.start_id.get_prev()
            setattr(prevbook, 'end_id', new_endpage)
            prevbook.save()
        except Archive.DoesNotExist:
            return None
    """ 
    
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

    
    