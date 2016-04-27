from django.contrib import admin, messages
import os
from django.conf import settings
from django.core.files import File
from django.core.files.images import ImageFile

# Register your models here.
from .models import Intro, CastEntry

class CastEntryAdmin(admin.ModelAdmin):
    fields = ["title",]
    list_display = ("title")
    

admin.site.register(Intro)
admin.site.register(CastEntry)

