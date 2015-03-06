__author__ = 'anmekin'
from celery import task
from django.conf import settings
from models import *
from utilities import *
import datetime
import flickrapi
import random
import time

@task(ignore_result=True, name='tasks.update_flickr_user')
def update_flickr_user(min_fave_date=0, flickruser=None):
    api_key = settings.SOCIAL_AUTH_FLICKR_KEY
    api_secret = settings.SOCIAL_AUTH_FLICKR_SECRET
    flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')
    active_users = FlickrUser.objects.filter(user__isnull=False)
    if flickruser is None:
        photos = Photo.objects.filter(favorited__in=active_users)
        users = FlickrUser.objects.filter(favorited__in=photos).\
            distinct().order_by('last_get_faved')
        try:
            flickruser = users[0]
        except IndexError:
            print "Empty flickrUsers List"
            return
    print "I choose flickrUser with id: %s" % flickruser.id
    # user = FlickrUser.objects.get(user_id=user_id)
    if flickruser.last_get_faved and not min_fave_date:
        min_fave_date = flickruser.last_get_faved
    photos = flickr.favorites.getList(user_id=flickruser.nsid,
                                      min_fave_date=min_fave_date,
                                      per_page=100,
                                      extras='url_l, url_z, url_c')
    flickruser.last_get_faved = int(time.time())
    flickruser.save()
    if 'photos' not in photos:
        print "Wrong response from Flickr"
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
        liking, created = Liking.objects.get_or_create(photo=_photo, user=flickruser)
        if created:
            liking.date_faved = dt
            liking.save()


@task(ignore_result=True, name='tasks.update_photo')
def update_photo():
    api_key = settings.SOCIAL_AUTH_FLICKR_KEY
    api_secret = settings.SOCIAL_AUTH_FLICKR_SECRET
    flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')
    photos = Photo.objects.all().order_by('last_get_faved')
    try:
        photo = photos[0]
    except IndexError:
        print "Empty photos list"
        return
    print "I choose photo with id: %s"% photo.id
    users = flickr.photos.getFavorites(photo_id=photo.id, per_page=100)
    photo.last_get_faved = int(time.time())
    photo.save()
    if 'photo' not in users:
        print "Wrong response from Flickr"
        return
    users = users['photo']['person']
    for user in users:
        _user, created = FlickrUser.objects.get_or_create(nsid=user['nsid'])
        dt = datetime.datetime.fromtimestamp(float(user['favedate']))
        liking, created = Liking.objects.get_or_create(photo=photo, user=_user)
        if created:
            liking.date_faved = dt
            liking.save()