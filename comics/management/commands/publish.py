from django.core.management.base import BaseCommand, CommandError
from comics.models import Comic, ComicFile, UploadedComicFile
from django.utils.dateparse import parse_date
from datetime import datetime
from django.conf import settings
from twython import Twython, TwythonError

class Command(BaseCommand):
    help = "Finds a comic with today's date and sets it to published. After that, it makes social media posts about it."
    
    def add_arguments(self, parser):
        parser.add_argument('date', nargs='?', default=datetime.today())
        #parser.add_argument('time_of_day')
        
    def handle(self, *args, **options):
        thedate = options['date']
        #thedate = datetime.today()
        try:
            comic = Comic.objects.get(date=thedate)
        except Comic.DoesNotExist:
            raise CommandError('Comic for %s does not exist' % str(day))
            
        # commented out all the old stuff
        result = comic.publish()
        if result == True:
            comic.tweet_comic()
            comic.facebook_comic()
