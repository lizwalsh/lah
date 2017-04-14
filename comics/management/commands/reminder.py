from django.core.management.base import BaseCommand, CommandError
from comics.models import Comic
from django.utils.dateparse import parse_date
from datetime import datetime
from django.conf import settings
from twython import Twython, TwythonError

class Command(BaseCommand):
    help = "Publishes the next available comic (on today's date)"
    
    def add_arguments(self, parser):
        #parser.add_argument('date', nargs='?', default=datetime.today())
        parser.add_argument('tod')
        
    def handle(self, *args, **options):
        thedate = datetime.today()
        tod = options['tod']
        try:
            comic = Comic.objects.get(date=thedate)
            comic.tweet_comic_reminder(tod)
        except Comic.DoesNotExist:
            raise CommandError('Comic for %s does not exist' % str(day))
            
        # commented out all the old stuff
        #result = comic.publish()
        #if result == True:
            #comic.tweet_comic_reminder()
