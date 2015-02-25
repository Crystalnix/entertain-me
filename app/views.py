"""
Module for views
"""
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required

from models import *
from utilities import update_with_weight, choose_photo_URL
from search_algorithm import *
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
    flickr = flickrapi.FlickrAPI(api_key, api_secret, format='json')
    my_id = request.user.username  # '130664317@N04'

    update_user_likes(flickr, my_id)
    rec_users = get_recomended_users(flickr, my_id)
    rec_photos = get_recomended_photos(flickr, rec_users, my_id)
    return render(request, 'index.html', {'photos': rec_photos[0:15]})


def show_fotos(request):
    photos = Photo.objects.all()
    return render(request, 'index.html', {'photos': photos[0:5]})

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')
