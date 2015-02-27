__author__ = 'anmekin'
from celery import task
from django.conf import settings
from models import *
from utilities import *
import datetime
import flickrapi
import random

@task(ignore_result=True, name='tasks.update_flickr_user')
def update_flickr_user(min_fave_date=0):
    api_key = settings.SOCIAL_AUTH_FLICKR_KEY
    api_secret = settings.SOCIAL_AUTH_FLICKR_SECRET
    flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')
    try:
        flickr_user = random.choice(FlickrUser.objects.all())
    except IndexError:
        print "List of users is Empty"
        return
    print "I choose Flickr User with id: %s"% flickr_user.id
    # user = FlickrUser.objects.get(user_id=user_id)
    if flickr_user.last_get_faved and not min_fave_date:
        min_fave_date = flickr_user.last_get_faved
    photos = flickr.favorites.getList(user_id=flickr_user.nsid,
                                      min_fave_date=min_fave_date,
                                      per_page=100,
                                      extras='url_l, url_z, url_c')
    if not photos.has_key('photos'):
        return
    photos = photos["photos"]["photo"]
    for photo in photos:
        _photo, created = Photo.objects.get_or_create(id=int(photo['id']))
        if created:
            url = choose_photo_URL(photo)
            _photo.owner = photo['owner']
            _photo.url = url
            _photo.save()
        dt = datetime.datetime.fromtimestamp(float(photo['date_faved']))
        liking, created = Liking.objects.get_or_create(photo=_photo, user=flickr_user)
        if created:
            liking.date_faved = dt
            liking.save()


@task(ignore_result=True, name='tasks.update_photo')
def update_photo():
    api_key = settings.SOCIAL_AUTH_FLICKR_KEY
    api_secret = settings.SOCIAL_AUTH_FLICKR_SECRET
    flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')
    try:
        photo = random.choice(Photo.objects.all())
    except IndexError:
        print "List of photo is Empty"
        return
    print "I choose photo with id: %s"% photo.id
    #photo = Photo.objects.get(id=id)
    users = flickr.photos.getFavorites(photo_id=photo.id, per_page=100)
    if not users.has_key('photo'):
        print 'Wrong photo_id'
        return
    users = users['photo']['person']
    for user in users:
        _user, created = FlickrUser.objects.get_or_create(nsid=user['nsid'])
        dt = datetime.datetime.fromtimestamp(float(user['favedate']))
        liking, created = Liking.objects.get_or_create(photo=photo, user=_user)
        if created:
            liking.date_faved = dt
            liking.save()
