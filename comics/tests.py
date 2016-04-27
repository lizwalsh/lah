import datetime, sys

from django.utils import timezone
from django.test import TestCase
from django.conf import settings
from django.core.urlresolvers import reverse

from .models import Comic, UploadedComicFile, ComicFile, GuestComic

def create_comic(is_pub, title, date, slug, cid, guest):
    """
    Creates a comic with the c_id, if it's published, title, date, previous and next comics, and url of comic file
    """
    return Comic.objects.create(published=is_pub,
                                title=title,
                                date=date,
                                slug=slug,
                                cid=cid,
                                guest=guest)
    
class ComicMethodTests(TestCase):
    
    def test_was_published_recently_with_future_comic(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_comic = Comic(date=time)
        self.assertEqual(future_comic.was_published_recently(), False)
        
    def test_was_published_recently_with_old_comic(self):
        time = timezone.now() - datetime.timedelta(days=30)
        old_comic = Comic(date=time)
        self.assertEqual(old_comic.was_published_recently(), False)
        
    def test_was_published_recently_with_recent_comic(self):
        time = timezone.now() - datetime.timedelta(hours=1)
        recent_comic = Comic(date=time)
        self.assertEqual(recent_comic.was_published_recently(), True)
        
    # test the first link 
    def test_get_first(self):
        first_comic = Comic(date="2016-01-01", published=True, cid=1)
        second_comic = Comic(date="2016-02-01", published=True, cid=2)
        first_comic.save()
        first_comic = Comic.objects.filter(cid=1)[0]
        second_comic.save()
        second_comic = Comic.objects.filter(cid=2)[0]
        self.assertEqual(first_comic.get_first(), None)
        self.assertEqual(second_comic.get_first(), first_comic)
    
    # test the previous link
    def test_get_prev(self):
        first_comic = Comic(date="2016-01-01", published=True, cid=1)
        second_comic = Comic(date="2016-03-01", published=True, cid=2)
        first_comic.save()
        first_comic = Comic.objects.filter(cid=1)[0]
        second_comic.save()
        second_comic = Comic.objects.filter(cid=2)[0]
        self.assertEqual(first_comic.get_prev(), None)
        self.assertEqual(second_comic.get_prev(), first_comic)
    
    def test_get_next(self):
        first_comic = Comic(date="2016-01-01", published=True, cid=1)
        second_comic = Comic(date="2016-03-01", published=True, cid=2)
        first_comic.save()
        first_comic = Comic.objects.filter(cid=1)[0]
        second_comic.save()
        second_comic = Comic.objects.filter(cid=2)[0]
        self.assertEqual(second_comic.get_next(), None)
        self.assertEqual(first_comic.get_next(), second_comic)
        
    def test_get_latest(self):
        first_comic = Comic(date="2016-01-01", published=True, cid=1)
        second_comic = Comic(date="2016-03-01", published=True, cid=2)
        first_comic.save()
        first_comic = Comic.objects.filter(cid=1)[0]
        second_comic.save()
        second_comic = Comic.objects.filter(cid=2)[0]
        self.assertEqual(second_comic.get_latest(), None)
        self.assertEqual(first_comic.get_latest(), second_comic)
    
    def test_renumber(self):
        first_comic = Comic(date="2016-02-01", published=True, cid=1)
        second_comic = Comic(date="2016-03-01", published=True, cid=2)
        third_comic = Comic(date="2016-01-01", published=True, cid=3) # note the cid and the date!
        first_comic.save()
        second_comic.save()
        third_comic.save()
        # this is where the magic happens
        third_comic.renumber()
        first_comic = Comic.objects.filter(date="2016-02-01")[0]
        second_comic = Comic.objects.filter(date="2016-03-01")[0]
        third_comic = Comic.objects.filter(date="2016-01-01")[0]
        self.assertEqual(third_comic.cid, 1)
        self.assertEqual(first_comic.cid, 2)
        self.assertEqual(second_comic.cid, 3)
    
    # this is going to be difficult
    # need to test this way:
    # publish a comic that doesn't exist
    # publish a comic that does exist but with no file
    # publish a comic that does exist with a file
    # publish a comic already published
    def test_publish(self):
        # test one: publish comic with no file
        first_comic = Comic(date="2016-02-01", published=False, cid=1)
        self.assertEqual(first_comic.publish(), False)
        
        # test two: publish comic with a file
        first_comic.save()
        first_comic = Comic.objects.filter(cid=1)[0]
        comic_page = UploadedComicFile(comic=first_comic,upload="pageX.jpg", alt_text="Foo")
        comic_page.save()
        self.assertEqual(first_comic.publish(), True)
        
        # test three: publish comic that's already published
        self.assertEqual(first_comic.publish(), False)
    
    def test_tweet(self):
        first_comic = Comic(date="2016-02-01", published=False, cid=1)
        self.assertEqual(first_comic.tweet_comic(), False)
        

class ComicViewTests(TestCase):
    fixtures = ['comics_views_testdata.json']
    
    def test_index(self):
        resp = self.client.get('/comics/')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('comic' in resp.context)
        comic = resp.context['comic']
        self.assertEqual([comic.pk],[1])
        

        
class ComicPageTests(TestCase):
    
    def test_page_view(self):
        tnow = timezone.now()
        past_comic = create_comic(True, "Hey", tnow - datetime.timedelta(days=1), "hi-hey", 1, False)
        response = self.client.get(reverse('comics:page', args=(past_comic.id, past_comic.slug,)))
        self.assertEqual(response.status_code, 200)
        response = self.client.get('10/hi-there/')
        self.assertEqual(response.status_code, 404)

# Create your tests here.
