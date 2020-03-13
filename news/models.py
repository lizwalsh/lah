import datetime, os

from django.utils import text, timezone
from django.db import models
from django.conf import settings
# use this if you use ckeditor
from ckeditor.fields import RichTextField

class NewsItem(models.Model):
    date = models.DateTimeField()
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, null=True)
    published = models.BooleanField()
    draft = models.BooleanField(default=True)
    # comment this out if you use ckeditor
    # news = models.TextField()
    # use this if you use ckeditor
    news = RichTextField()
    
    class Meta:
        verbose_name_plural = 'News items'
        
    def __str__(self):
        return "News for " + str(self.date)

    def publish(self):
        news = self
        setattr(news, 'published', True)
        
    def prep(self):
        news = self
        setattr(news, 'draft', False)