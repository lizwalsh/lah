from django.contrib import admin, messages
import os
from django.conf import settings

from .models import Comic, ComicFile, UploadedComicFile, GuestComic

def publish(comicadmin, request, queryset):
    for item in queryset:
        if item.published == False:
            result = item.publish()
            messages.success(request, result)
            #if result == True:
            #    messages.success(request, "Comic " + str(item.id) + " successfully published")
            #else:
            #    messages.error(request, "You cannot publish comic " + str(item.id) + " because you haven't uploaded a comic for it yet.")
        else:
            messages.info(request, "Comic " + str(item.id) + " already published")

            

def unpublish(comicadmin, request, queryset):
    queryset.update(published=False)
    
def renumber(comicadmin, request, queryset):
    for item in queryset.order_by('date'):
        item.renumber()
    
   
publish.short_description = "Publish comics"
unpublish.short_description = "Unpublish comics"
renumber.short_description = "Renumber comics"

class ComicFileInline(admin.TabularInline):
    model = ComicFile
    extra = 1

class UploadedComicFileInline(admin.TabularInline):
    model = UploadedComicFile
    extra = 1
    
class GuestComicInline(admin.TabularInline):
    model = GuestComic
    extra = 1

class ComicAdmin(admin.ModelAdmin):
    list_display=['title', 'id', 'date', 'cid', 'published',]
    ordering=['-date', 'published', 'id']
    actions=[publish, unpublish, renumber]
    inlines = (UploadedComicFileInline, ComicFileInline, GuestComicInline )
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('cid',)
    
admin.site.register(Comic, ComicAdmin)