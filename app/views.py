from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from utilities import *
from models import *
from django.db.models import Sum
from tasks import update_flickr_user
import datetime


def oauth_callback(request):
    """
      | This function fetch Flickr auth response and create or update info of successfully authorized user.
      | You can't call it manually.
    """
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
      | Main page with recommended photos and possibility like it or look at next photo.
      | Work with GET and AJAX requests.
    """
    delta_time = datetime.datetime.now() - datetime.timedelta(days=7)
    me = FlickrUser.objects.get(user=request.user)
    my_favs = Photo.objects.filter(favorited=me)
    reviewed = Photo.objects.filter(reviewed=me)
    rec_users = FlickrUser.objects.filter(favorited__in=my_favs).distinct().exclude(id=me.id)
    rec_photo = Photo.objects.filter(favorited__in=rec_users, liking__date_faved__gt=delta_time).exclude(id__in=my_favs | reviewed).\
        filter(favorited__to_weight__against=me).distinct().\
        annotate(sum=Sum('favorited__to_weight__weight')).order_by('-sum').first()
    if rec_photo:
        review, created = Review.objects.get_or_create(photo=rec_photo, user=me)
    else:
        msg = "Photos not found. Probably you didn't like anything on Flickr. " \
              "Try to like anything and "
        return render(request, 'recommended.html', {'error_msg': msg})
    if request.is_ajax():
        response = {'url': rec_photo.url, 'id': rec_photo.id}
        return JsonResponse(response)    # should return json
    return render(request, 'recommended.html', {'photo': rec_photo})


def auth(request):
    """
      |  Page for unauthorized users.
      |  You can authorize with Flickr here.
    """
    return render(request, 'auth.html')


def logout(request):
    """
      |  Logout.
    """
    auth_logout(request)
    return HttpResponseRedirect('/')


def update(request):
    # Need some protection
    me = FlickrUser.objects.get(user=request.user)
    update_flickr_user(flickruser=me)
    return HttpResponseRedirect('/')


def test(request):
    msg = "Photos not found. Probably you didn't like anything on Flickr. " \
          "Try to like anything and "
    return render(request, 'recommended.html', {'error_msg': msg})

def test_exception(request):
    pass
    # try:
    #     raise Exception
    # except Exception:
    #     return HttpResponse("OK")
