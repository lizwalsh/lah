from django.contrib import admin
from django.core import urlresolvers

from photologue.models import Photo, PhotoEffect, Watermark
from .models import Fanart, InfoType

class FanartAdmin(admin.ModelAdmin):
    list_display=['photo_title', 'author', 'date_added', 'id', ]
    ordering = ['photo__title']
    
    def photo_title(self, obj):
        return obj.photo.title
    photo_title.short_description = 'Title'
    photo_title.admin_order_field = 'photo__title'


class InfoTypeAdmin(admin.ModelAdmin):
    list_display=['title', 'type', 'desc', 'id',]

# unregister stuff we don't need
admin.site.unregister(PhotoEffect)
admin.site.unregister(Watermark)

admin.site.register(Fanart, FanartAdmin)
admin.site.register(InfoType, InfoTypeAdmin)