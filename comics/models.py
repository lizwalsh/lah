import datetime, os
import facebook

from django.utils import text, timezone
from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify
from django.core.files import File
from django.core.files.images import ImageFile
from django.urls import reverse
from twython import Twython, TwythonError

class Comic(models.Model):
    date = models.DateField('date published')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, null=True)
    published = models.BooleanField('is published', default=False)
    
    # try this for those occasional guest comics
    cid = models.IntegerField('Comic number', default=0)
    guest = models.BooleanField('Is guest/special comic', default=False)
    
    def __str__(self):
        if self.guest == False:
            return "Comic " + str(self.cid) + " - " + self.title + " - " + str(self.date)
        else:
            return str(self.gcomic) + " - " + self.title + " - " + str(self.date)
            # different types of "guest" comics               
    
    # get URL for comic
    def get_url(self):
        return '/' + str(self.id) + '/' + self.slug
    
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.date <= now
    
    def get_first(self):
        try:
            comix = Comic.objects.filter(published=True).earliest()
            if self.date == comix.date:
                comix = None
        except Comic.DoesNotExist:
            comix = None
        except IndexError:
            comix = None
        return comix
    
    def get_prev(self):
        try:
            prev = Comic.objects.filter(published=True, date__lt=self.date).order_by('-date')[0]
        except Comic.DoesNotExist:
            prev = None
        except IndexError:
            prev = None
        return prev
    
    def get_next(self):
        try:
            next = Comic.objects.filter(published=True, date__gt=self.date).order_by('date')[0]
        except Comic.DoesNotExist:
            next = None
        except IndexError:
            next = None
        return next
    
    def get_latest(self):
        try:
            comix = Comic.objects.filter(published=True).latest()
            if self.date == comix.date:
                comix = None
        except Comic.DoesNotExist:
            comix = None
        except IndexError:
            comix = None
        return comix

    
    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
        super(Comic, self).save(*args, **kwargs)
        
    def renumber(self):
        # defaults to 1 at the beginning of a list
        # now we go through the rest of everything and make numbers happen
        current = self
        # yay for linked lists
        while current is not None:
            # don't renumber guest comics
            if current.guest == False:
                try:
                    # filter out all guest comics
                    old_num = Comic.objects.filter(guest=False, published=True, date__lt=current.date).order_by('-date')[0].cid
                except Comic.DoesNotExist:
                    # beginning of list
                    old_num = 0
                except IndexError:
                    old_num = 0
                current.cid = old_num + 1
                current.save()
            current = current.get_next()
            
    # put the code for publishing a comic here
    def publish(self):
        comic = self
        pages = UploadedComicFile.objects.filter(comic=comic.id)
        if len(pages) > 0:
            has_page = 0
            for one in pages:
                if one.upload:
                    # copy some love
                    pub_file = ComicFile()
                    pub_file.comic = one.comic
                    pub_file.alt_text = one.alt_text
                    pub_file.page = ImageFile(one.upload, one.upload.name)
                    pub_file.save()
                    one.upload.close()
                    has_page = 1
                else:
                    #messages.error(request, "You cannot publish comic " + str(comic.id) + " because you haven't uploaded a comic for it yet.")
                    return False
    
            if has_page == 1:
                setattr(comic, 'published', True)
                if comic.guest == False:
                    comic.renumber()
                comic.save()
                # this is where I need to do next/prev stuff
                pages.delete()
                #messages.success(request, "Comic " + str(comic.id) + " successfully published")
                return True
            else:
                return False
        else:
            return False
        
        
    # function for publishing a comic
    def tweet_comic(self):
        date = self.date
        # now tweet this mofo
        twitter = Twython(settings.APP_KEY, settings.APP_SECRET, settings.OAUTH_TOKEN, settings.OAUTH_TOKEN_SECRET)
        
        try:
            twitter.update_status(status='New comic for ' + str(date) + '! https://lifesahowl.com/ #webcomics')
        except TwythonError as e:
            print(e)
            
        # twitter stuff to keep handy
        """
         # now let's tweet this mofo
        APP_KEY = settings.APP_KEY
        APP_SECRET = settings.APP_SECRET
        
        twitter = Twython(APP_KEY, APP_SECRET)
        auth = twitter.get_authentication_tokens()
        OAUTH_TOKEN = auth['oauth_token']
        OAUTH_TOKEN_SECRET = auth['oauth_token_secret']
        
        twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
        oauth_verifier_url = auth['auth_url']
        oauth_verifier = requests.get(oauth_verifier_url)
        
        final_step = twitter.get_authorized_tokens(oauth_verifier)
        
        OAUTH_TOKEN = final_step['oauth_token']
        OAUTH_TOKEN_SECRET = final_step['oauth_token_secret']
        
        twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
        
        try:
            twitter.update_status(status='Read my comic, peoples!')
        except TwythonError as e:
            print(e)
        """
    def tweet_comic_reminder(self, tod):
        date = self.date
        
        # now tweet this mofo
        twitter = Twython(settings.APP_KEY, settings.APP_SECRET, settings.OAUTH_TOKEN, settings.OAUTH_TOKEN_SECRET)
        
        
        # let's get some reminders
        
        if tod == "morning":
            status = "Good morning! New comic for " + str(date) + "! https://lifesahowl.com"
        elif tod == "afternoon":
            status = "Afternoon reminder! New comic for " + str(date) + "! https://lifesahowl.com"
        elif tod == "evening":
            status = "Evening reminder! New comic for " + str(date) + "! https://lifesahowl.com"
        elif tod == "reminder":
            status = "Reminder that there's a new comic today, " + str(date) + "! https://lifesahowl.com #webcomics"
        try:
            twitter.update_status(status=status)
        except TwythonError as e:
            print(e)
                
                
    # now let's set this up as a Facebook post!
    # code taken from http://nodotcom.org/python-facebook-tutorial.html
    def facebook_comic(self):
        date = self.date
        # cfg page_id, access_token
        # we supply these in settings
        graph = facebook.GraphAPI(settings.FB_ACCESS_TOKEN)
        resp = graph.get_object('me/accounts')
        page_access_token = None
        for page in resp['data']:
            if page['id'] == settings.FB_PAGE_ID:
                page_access_token = page['access_token']
        graph = facebook.GraphAPI(page_access_token)
        
        # now let's work on the message
        # we need a comment like Tweeting, but we want to add the current comic page?
        # how's that work?
        message = 'New comic for ' + str(date) + '!'
        comicFile = ComicFile.objects.filter(comic_id = self.id)[0]
        attachment = {
            'link': settings.SITE_URL + reverse('comics:page', args=(self.pk, self.slug )),
            'picture': settings.SITE_URL + settings.MEDIA_URL + comicFile.page.name,
        }
        status = graph.put_wall_post(message=message,attachment=attachment)
        #print(attachment['link'])
                
    class Meta:
        ordering = ('-date',)
        get_latest_by = ('date')
        
    
    
    
# class for published comics
class ComicFile(models.Model):
    
    comic = models.ForeignKey(Comic, on_delete=models.CASCADE)
    page = models.ImageField(upload_to=settings.COMICS_F + "/", blank=True)
    alt_text = models.TextField(null=True)
    
    
    def __str__(self):
        return "Comic file " + str(self.id) + " for comic #" + str(self.comic)


# class for uploaded comics
# uploads and published have the same fields, except published files get put in a differenet folder
class UploadedComicFile(models.Model):
    comic = models.ForeignKey(Comic, on_delete=models.CASCADE)
    # if there are issues, I can make upload blank=True again
    upload = models.ImageField(upload_to=settings.UPLOAD_F + "/")
    alt_text = models.TextField(null=True)
    
    def __str__(self):
        return "Uploaded comic file " + str(self.id) + " for comic #" + str(self.comic)
    
    def delete(self, *args, **kwargs):
        if os.path.isfile(self.upload_file.path):
            os.remove(self.upload_file.path)
        self.upload.delete()
        super(UploadedComicFile, self).delete(*args, **kwargs)
        
        
# class for guest comic details
# guest comics only apply if the comic's guest value is True
class GuestComic(models.Model):
  
    type = models.CharField(max_length=10, choices=[('guest', 'Guest comic'), ('special', 'Special item'), ('art', 'Filler art'), ('ad', 'Advertisement'), ] )
    author = models.CharField(max_length=100, blank=True)
    url = models.URLField(max_length=200, blank=True)
    ref_comic = models.OneToOneField(Comic, related_name='gcomic', on_delete=models.CASCADE)
    
    
    def __str__(self):
        #return '{} by {}'.format(self.ctype(), self.author)
        return self.get_type_display() + ' by ' + self.author
    
    