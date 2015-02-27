"""
Module for views
"""
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required

from search_algorithm import *
import json
import flickrapi
import random


def auth(request):
    return render(request, 'auth.html')

def oauth_callback(request):
    flickruser, created = FlickrUser.objects.get_or_create(nsid='130664317@N04')
                                            # flickr nsid != request.user.username, should find it in user
    if created:
        flickruser.user = request.user
    print request.user.username
    return HttpResponseRedirect('/')

def home(request):
    api_key = settings.SOCIAL_AUTH_FLICKR_KEY
    api_secret = settings.SOCIAL_AUTH_FLICKR_SECRET

    flickr = flickrapi.FlickrAPI(api_key, api_secret, format='json')
    photos = flickr.favorites.getList(user_id='130664317@N04',
                                      per_page='10',
                                      extras='url_m')

    return render(request, 'index.html')

@login_required()
def recomended(request):
    """
    Algorithm which suggests photos to user based on user's likes
    and likes of people who also liked the same as user did
    """
    api_key = settings.SOCIAL_AUTH_FLICKR_KEY
    api_secret = settings.SOCIAL_AUTH_FLICKR_SECRET
    flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')
    my_id = '130664317@N04'        # flickr nsid != request.user.username, should find it in user

    update_user_likes(flickr, my_id)
    rec_users = get_recommended_users(flickr, my_id)
    rec_photos = get_recommended_photos(flickr, rec_users, my_id)
    return render(request, 'index.html', {'photos': rec_photos[0:15]})


def show_photos(request):
    photos = Photo.objects.all()
    return render(request, 'index.html', {'photos': photos[0:5]})

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')

def update_photo(request):
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
        return HttpResponse('not ok')
    users = users['photo']['person']
    for user in users:
        _user, created = FlickrUser.objects.get_or_create(nsid=user['nsid'])
        dt = datetime.datetime.fromtimestamp(float(user['favedate']))
        liking, created = Liking.objects.get_or_create(photo=photo, user=_user)
        if created:
            liking.date_faved = dt
            liking.save()
    return HttpResponse('ok')





