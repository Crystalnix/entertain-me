__author__ = 'anmekin'

import flickrapi
from models import *
from django.conf import settings
from django.utils import timezone
from flickrapi.auth import FlickrAccessToken
from django.http import JsonResponse, HttpResponse

def like(request):
    if request.is_ajax():
    #     id = data #!!!!
    # Try to find photo in user_favorites
        id = '6304393890'
        api_key = settings.SOCIAL_AUTH_FLICKR_KEY
        api_secret = settings.SOCIAL_AUTH_FLICKR_SECRET
        d = request.user.social_auth.first().tokens
        token = FlickrAccessToken(token=d['oauth_token'], token_secret=d['oauth_token_secret'], access_level=u'write',
                 fullname=d['fullname'], username=d['username'], user_nsid=d['user_nsid'])
        flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json', username=u'anmekin', token=token) # , token=u'72157650494242720-81ccb4e70d57cac9'
        flickr.favorites.add(photo_id=id)
        me = FlickrUser.objects.get(user=request.user)
        photo = Photo.objects.get(id=id)
        dt = timezone.now().replace(second=0, microsecond=0)
        liking, created = Liking.objects.get_or_create(user=me, photo=photo)
        if created:
            liking.date_faved = dt
            liking.save()
        return JsonResponse({'stat': 'ok'})

        # Set last_get_faved = 0 from liked photo
    return HttpResponse("This is not JSON!")