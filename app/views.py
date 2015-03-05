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
    me = FlickrUser.objects.get(user=request.user)
    my_favs = Photo.objects.filter(favorited=me)
    reviewed = set(Photo.objects.filter(reviewed=me))
    rec_users = get_recommended_users(me, my_favs)  # return QuerySet
    rec_photos = get_recommended_photos(rec_users, my_favs, reviewed)
    rec_photo = rec_photos[0]
    review, created = Review.objects.get_or_create(photo=rec_photo, user=me)
    if request.is_ajax():
        str = "{'4':1,'a':2}"
        return HttpResponse('<img src=%s/>' % rec_photo.url, "text/html")    # -
        #return HttpResponse('<a href=#>Link</a>' , "text/html")            # +
        #return HttpResponse('<a href=%s>Link</a>' % (rec_photo.url), "text/html") # +
    return render(request, 'recomended.html', {'photo': rec_photo})


def test_ajax(request):
    photo = Photo.objects.get(id=14148937246)
    if request.is_ajax():
        # str = "{'4':1,'a':2}"
        #return HttpResponse('<img href=%s>/>' % rec_photo, "text/html")    # -
        #return HttpResponse('<a href=#>Link</a>' , "text/html")            # +
        link = "http://ya.ru"
        str='<a href=%s>Link</a>' % (photo.url)
        return HttpResponse(str, "text/html")

def show_photos(request):
    photos = Photo.objects.all()
    return render(request, 'index.html', {'photos': photos[0:5]})


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')



