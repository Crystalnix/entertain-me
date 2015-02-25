"""
Module for views
"""
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required

from models import *
from utilities import update_with_weight, choose_photo_URL
import datetime
import json
import flickrapi
#from social_auth.models import UserSocialAuth


def auth(request):
#    print UserSocialAuth.objects.filter(provider='flickr').get(id='1').tokens
    return render(request, 'auth.html')


def home(request):
    #print request.user.username
    api_key = settings.SOCIAL_AUTH_FLICKR_KEY
    api_secret = settings.SOCIAL_AUTH_FLICKR_SECRET

    flickr = flickrapi.FlickrAPI(api_key, api_secret, format='json')
    photos = flickr.favorites.getList(user_id='130664317@N04',
                                      per_page='10',
                                      extras='url_m')
    photos = json.loads(photos)
    print photos["photos"]["photo"]
    # photo = flickr.photos.getSizes(photo_id='16580157821')
    # print photo

    return render(request, 'index.html', {'photos': photos["photos"]["photo"]})

@login_required()
def recomended(request):
    """
    lgorithm which suggests photos to user based on user's likes
    and likes of people who also liked the same as user did
    """
    api_key = settings.SOCIAL_AUTH_FLICKR_KEY
    api_secret = settings.SOCIAL_AUTH_FLICKR_SECRET
    req_counter = 0

    flickr = flickrapi.FlickrAPI(api_key, api_secret, format='json')
    my_id = request.user.username#'130664317@N04'
    user, created = User.objects.get_or_create(user_id=my_id)
    req_counter += 1
    photos = flickr.favorites.getList(user_id=my_id,
                                      extras='url_l, url_z, url_c')
    photos = json.loads(photos)
    photos = photos["photos"]["photo"]
    for photo in photos:
        url = choose_photo_URL(photo)
        _photo, created = Photo.objects.get_or_create(id=int(photo['id']),
                                                      owner=photo['owner'], url=url)
        dt = datetime.datetime.fromtimestamp(float(photo['date_faved']))
        liking, created = Liking.objects.get_or_create(photo=_photo, user=user, date_faved=dt)

    rec_users = set()
    my_favs = Photo.objects.filter(user__user_id=my_id)
    my_favs_ids = [x.id for x in my_favs]
    for photo in my_favs:
        # photo is already db model
        req_counter += 1
        users = flickr.photos.getFavorites(photo_id=photo.id, per_page=10)
        users = json.loads(users)
        users = users['photo']['person']
        for user in users:
            _user, created = User.objects.get_or_create(user_id=user['nsid'])
            dt = datetime.datetime.fromtimestamp(float(user['favedate']))
            liking, created = Liking.objects.get_or_create(photo=photo, user=_user, date_faved=dt)
            rec_users.update({_user})
    print rec_users
    print len(rec_users)

    rec_photos = {}
    for user in rec_users:
        req_counter += 1
        photos = flickr.favorites.getList(user_id=user.user_id,
                                          extras='url_l, url_z, url_c', per_page=10)
        photos = json.loads(photos)
        photos = photos["photos"]["photo"]
        for photo in photos:
            url = choose_photo_URL(photo)
            _photo, created = Photo.objects.get_or_create(id=int(photo['id']),
                                                          owner=photo['owner'], url=url)
            dt = datetime.datetime.fromtimestamp(float(photo['date_faved']))
            liking, created = Liking.objects.get_or_create(photo=_photo, user=user, date_faved=dt)
        rec_photos = update_with_weight(rec_photos, photos, my_favs_ids)
    rec_photos = sorted(rec_photos.items(), key=lambda(k, v): v, reverse=True)
    rec_photos = [photo[0] for photo in rec_photos]
    res_photos = []
    for photo in rec_photos:
        res_photos.append(Photo.objects.get(id=photo))
    print req_counter
    return render(request, 'index.html', {'photos': res_photos[0:5]})


def show_fotos(request):
    photos = Photo.objects.all()
    return render(request, 'index.html', {'photos': photos[0:5]})

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')
