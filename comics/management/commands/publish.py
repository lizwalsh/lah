from django.core.management.base import BaseCommand, CommandError
from comics.models import Comic, ComicFile, UploadedComicFile
from django.utils.dateparse import parse_date
from datetime import datetime
from django.conf import settings
from twython import Twython, TwythonError

class Command(BaseCommand):
    help = "Tweets reminders that a comic has updated today."
    
    def add_arguments(self, parser):
        #parser.add_argument('date', nargs='?', default=datetime.today())
        parser.add_argument('time_of_day')
        
    def handle(self, *args, **options):
        #thedate = options['date']
        thedate = datetime.today()
        try:
            comic = Comic.objects.get(date=thedate)
        except Comic.DoesNotExist:
            raise CommandError('Comic for %s does not exist' % str(day))
            
        # commented out all the old stuff
        comic.tweet_comic_reminder(options['time_of_day'])
