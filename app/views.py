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


def auth(request):
    return render(request, 'auth.html')


def home(request):
    api_key = settings.SOCIAL_AUTH_FLICKR_KEY
    api_secret = settings.SOCIAL_AUTH_FLICKR_SECRET

    flickr = flickrapi.FlickrAPI(api_key, api_secret, format='json')
    photos = flickr.favorites.getList(user_id='130664317@N04',
                                      per_page='10',
                                      extras='url_m')
    photos = json.loads(photos)
    print photos["photos"]["photo"]

    return render(request, 'index.html', {'photos': photos["photos"]["photo"]})

@login_required()
def recomended(request):
    """
    Algorithm which suggests photos to user based on user's likes
    and likes of people who also liked the same as user did
    """
    api_key = settings.SOCIAL_AUTH_FLICKR_KEY
    api_secret = settings.SOCIAL_AUTH_FLICKR_SECRET
    flickr = flickrapi.FlickrAPI(api_key, api_secret, format='json')
    my_id = '130664317@N04'        # flickr nsid != request.user.username, should find him in user

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
