from django.db import models
from django.conf import settings
# use this if you use ckeditor
from ckeditor.fields import RichTextField

class AboutItem(models.Model):
    title = models.CharField(max_length=200)
    # comment this out if you use ckeditor
    # news = models.TextField()
    # use this if you use ckeditor
    body = RichTextField()
    
    class Meta:
        verbose_name_plural = 'About items'
        
    def __str__(self):
        return "About for " + str(self.title)