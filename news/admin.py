from django.contrib import admin, messages
import os
from django.conf import settings

from .models import NewsItem

class NewsItemAdmin(admin.ModelAdmin):
    fields = ["date", "title",]
    list_display = ("title")
    #actions=[publish, unpublish]
    
admin.site.register(NewsItem)