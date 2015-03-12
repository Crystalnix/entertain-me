"""
Module for views
"""
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required

import search_algorithm as sa
from models import *
from tasks import update_flickr_user
import time
import flickrapi
import json

def oauth_callback(request):
    try:
        nsid = request.user.social_auth.first().uid
    except AttributeError:
        return HttpResponse("Unknown Flickr account")
    flickruser, created = FlickrUser.objects.get_or_create(nsid=nsid)
    if created:
        flickruser.user = request.user
        flickruser.save()
    update_flickr_user(flickruser=flickruser)
    return HttpResponseRedirect('/')

@login_required()
def recommended(request):
    """
    Algorithm which suggests photos to user based on user's likes
    and likes of people who also liked the same as user did
    """
    me = FlickrUser.objects.get(user=request.user)
    my_favs = Photo.objects.filter(favorited=me)
    reviewed = set(Photo.objects.filter(reviewed=me))
    rec_users = sa.get_recommended_users(me, my_favs)
    rec_photos = sa.get_recommended_photos(rec_users, my_favs, reviewed)
    try:
        rec_photo = rec_photos[0]
    except IndexError:
        msg = "Photos not found. Probably you didn't like anything on Flickr. " \
              "Try to like anything and reauthentication on this website. " \
              "Also you can forget to run workers."
        return render(request, 'recommended.html', {'error_msg': msg})
    review, created = Review.objects.get_or_create(photo=rec_photo, user=me)
    if request.is_ajax():
        response = {'url': rec_photo.url, 'id': rec_photo.id}
        return JsonResponse(response)    # should return json
    return render(request, 'recommended.html', {'photo': rec_photo})


def auth(request):
    return render(request, 'auth.html')

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')

