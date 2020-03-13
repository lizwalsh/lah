from django.contrib import admin, messages
import os
from django.conf import settings

from .models import NewsItem

def publish(newsadmin, request, queryset):
    for item in queryset:
        if item.published == False:
            # if we're publishing from the command line, we want to de-draft everything too
            result = item.prep()
            result = item.publish()
            messages.success(request, result)
        else:
            messages.info(request, "News item " + str(item.id) + " already published")
            
            
def ready_for_publishing(newsadmin, request, queryset):
    for item in queryset:
        if item.draft == True:
            result = item.prep()
            messages.success(request, reset)
        else:
            messages.info(request, "News item " + str(item.id) + " already ready for publishing")
            
def unpublish(newsadmin, request, queryset):
    queryset.update(published=False,draft = True)
            
publish.short_description = "Publish news items"
ready_for_publishing.short_description = "Ready news items for publishing"
unpublish.short_description = "Unpublish news items"

class NewsItemAdmin(admin.ModelAdmin):
    fields = ["date", "title",]
    list_display = ("title")
    #actions=[publish, unpublish]
    
admin.site.register(NewsItem)