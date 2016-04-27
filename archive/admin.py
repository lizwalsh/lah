from django.contrib import admin, messages
import os
from django.conf import settings

from .models import Archive

def new_book(archiveadmin, request, queryset):
    return "foo"


class ArchiveAdmin(admin.ModelAdmin):
    list_display=['title', 'booknum',]
    #readonly_fields = ('end_id',)
    
admin.site.register(Archive, ArchiveAdmin)