"""
Module for views
"""
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from utilities import *
from models import *
from django.db.models import Sum
from tasks import update_flickr_user


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
    reviewed = Photo.objects.filter(reviewed=me)
    rec_users = FlickrUser.objects.filter(favorited__in=my_favs).distinct().exclude(id=me.id)
    rec_photo = Photo.objects.filter(favorited__in=rec_users).exclude(id__in=my_favs | reviewed).\
        filter(favorited__to_weight__against=me).distinct().\
        annotate(sum=Sum('favorited__to_weight__weight')).order_by('-sum').first()
    if rec_photo:
        review, created = Review.objects.get_or_create(photo=rec_photo, user=me)
    else:
        msg = "Photos not found. Probably you didn't like anything on Flickr. " \
              "Try to like anything and reauthentication on this website. " \
              "Also you can forget to run workers."
        return render(request, 'recommended.html', {'error_msg': msg})
    if request.is_ajax():
        response = {'url': rec_photo.url, 'id': rec_photo.id}
        return JsonResponse(response)    # should return json
    return render(request, 'recommended.html', {'photo': rec_photo})


def auth(request):
    return render(request, 'auth.html')


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')
