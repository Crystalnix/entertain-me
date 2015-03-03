"""
Module for views
"""
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required

from search_algorithm import *
from models import *
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
    rec_users = get_recommended_users(my_id)
    rec_photos = get_recommended_photos(rec_users, my_id)
    try:
        rec_photo = rec_photos[0]
        msg = "Recommended photo for you"
    except IndexError:
        rec_photo = random.choice(Photo.objects.all()).url
        msg = "Sorry, we can't choose something for you. Keep the photo which can be like you"
    print rec_photo
    return render(request, 'recomended.html', {'photo': rec_photo, 'msg': msg})


def show_photos(request):
    photos = Photo.objects.all()
    return render(request, 'index.html', {'photos': photos[0:5]})

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')



