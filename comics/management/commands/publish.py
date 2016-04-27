from django.core.management.base import BaseCommand, CommandError
from comics.models import Comic, ComicFile, UploadedComicFile
from django.utils.dateparse import parse_date
from datetime import datetime
from django.conf import settings
from twython import Twython, TwythonError

class Command(BaseCommand):
    help = "Publishes the next available comic (on today's date)"
    
    def add_arguments(self, parser):
        parser.add_argument('date', nargs='?', default=datetime.today())
        
    def handle(self, *args, **options):
        thedate = options['date']
        try:
            comic = Comic.objects.get(date=thedate)
        except Comic.DoesNotExist:
            raise CommandError('Comic for %s does not exist' % str(day))
            
        # commented out all the old stuff
        result = comic.publish()
        if result == True:
            comic.tweet_comic()
