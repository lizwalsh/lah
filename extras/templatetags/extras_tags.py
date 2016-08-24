from django import template

from ..models import Gallery
from ..models import Photo

register = template.Library()


@register.inclusion_tag('extras/tags/imgshort.html')
def next_in_gallery(photo, gallery):
    return {'photo': photo.get_next_in_gallery(gallery)}


@register.inclusion_tag('extras/tags/imgshort.html')
def previous_in_gallery(photo, gallery):
    return {'photo': photo.get_previous_in_gallery(gallery)}