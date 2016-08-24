from django.db import models
from django.conf import settings
from photologue.models import Gallery, Photo
from django.utils import formats
from django.utils.timezone import now
    
class Fanart(models.Model):
    photo = models.OneToOneField(Photo, related_name='fanpiece')
    author = models.CharField(max_length=100, blank=True)
    url = models.URLField(max_length=200, blank=True)
    date_added = models.DateTimeField(default=now)
    
    def __str__(self):
        return "Fanart '" + self.photo.title + "' done by " + self.author + " - added " + str( formats.date_format(self.date_added, "SHORT_DATETIME_FORMAT") )
    
    def save(self, *args, **kwargs):
        super(Fanart, self).save(*args, **kwargs)
        # let's add to the gallery too
        try:
            gallery = Gallery.objects.get(title='Fanart')
        except Gallery.DoesNotExist:
            gallery = None
        else:
            gallery.photos.add(self.photo)
            gallery.save()
            
class InfoType(models.Model):
    type = models.CharField(max_length=20, choices=[('media', 'Media coverage'), ('mycontrib', "Things I've done"), ('interesting', 'Interesting things'), ('fanworks', 'Fan works (not art)'), ] )
    title = models.CharField(max_length=200, blank=True)
    url = models.URLField(max_length=200, blank=True)
    desc = models.CharField(max_length=200, blank=True)
    
    def __str__(self):
        return "Info link - " + self.get_type_display() + " - " + self.title + " - " + self.desc