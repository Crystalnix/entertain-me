"""
Module for views
"""
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required

from search_algorithm import *
from models import *


def oauth_callback(request):
    flickruser, created = FlickrUser.objects.get_or_create(nsid='130664317@N04')
                                            # flickr nsid != request.user.username, should find it in user
    if created:
        flickruser.user = request.user
    print request.user.username
    return HttpResponseRedirect('/')

def home(request):
    return render(request, 'index.html')

@login_required()
def recommended(request):
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
        return HttpResponse('<img src=%s/>' % rec_photo.url, "text/html")    # +
    return render(request, 'recommended.html', {'photo': rec_photo})


def show_photos(request):
    photos = Photo.objects.all()
    return render(request, 'index.html', {'photos': photos[0:5]})


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')



