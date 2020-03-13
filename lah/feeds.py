from django.contrib.syndication.views import Feed
from django.core.files.base import File
from django.core.files.images import ImageFile
from django.utils.feedgenerator import Rss201rev2Feed
from comics.models import Comic, ComicFile


class ComicFeed(Rss201rev2Feed):
    def root_attributes(self):
        attrs = super(ComicFeed, self).root_attributes()
        attrs['xmlns:content'] = 'http://purl.org/rss/1.0/modules/content/'
        attrs['xmlns:dc'] = "http://purl.org/dc/elements/1.1/"
        return attrs
    
    def add_root_elements(self, handler):
        super(ComicFeed,self).add_root_elements(handler)
        handler.addQuickElement(u"copyright", "Copyright 2016 Liz Walsh")
        handler.startElement(u"image", {})
        handler.addQuickElement(u"url", "/common/comics/images/plain_logo.png")
        handler.addQuickElement(u"title", "Life's a Howl")
        handler.addQuickElement(u"link", "http://www.lifesahowl.com")
        handler.endElement(u"image")
    
    def add_item_elements(self, handler, item):
        super(ComicFeed, self).add_item_elements(handler, item)
        handler.addQuickElement(u'dc:creator', "Liz Walsh")
        handler.addQuickElement(u'content:encoded', item['content_encoded'])

        
class RecentUpdates(Feed):
    feed_type = ComicFeed
    title = "Life's a Howl"
    link = "https://lifesahowl.com/"
    description = "Werewolf webcomic - Epic urban fantasy about life, love and lycanthropy"
    feed_url = "/rss/"
    
    
    def items(self):
        # most recent comics
        return Comic.objects.filter(published=True).order_by('-date')[:6]
    
    def item_title(self, item):
        return '#' + str(item.id) + " - " + item.title
    
    def item_description(self, item):
        return "Comic update for " + str(item.date)
        
    def item_link(self, item):
        return "https://lifesahowl.com/" + str(item.id) + "/" + item.slug
    
    """
    def item_enclosures(self, item):
        images = []
        for thing in item.comicfile_set.all():
            images.append( Enclosure("http://127.0.0.1:8000" + thing.page.url, str(thing.page.size), "image/jpeg") )
        return images
    """
    
    
    def item_extra_kwargs(self, item):
        return {'content_encoded' : self.item_content_encoded(item)}
    
    def item_content_encoded(self, item):
        obj = item.comicfile_set.all()
        images = ""
        for thing in obj:
            images += '<img src="%s" width="%s" height="%s" />' % ("https://lifesahowl.com" + thing.page.url, thing.page.width, thing.page.height)
        return images
