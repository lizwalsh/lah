from django.conf import settings
from .models import Comic


def site(request):
    return {'my_site': settings.SITE_URL}


