__author__ = 'anmekin'
from models import *
from utilities import *
import datetime


def get_recommended_users(me, my_favs):
    users = FlickrUser.objects.filter(favorited__in=my_favs).distinct().exclude(user=me.user)
    return users


def get_recommended_photos(rec_users, my_favs, reviewed):
    rec_photos = {}
    for user in rec_users:
        photos = set(Photo.objects.filter(favorited=user))
        rec_photos = update_with_weight(rec_photos, photos, my_favs, reviewed)
    rec_photos = sorted(rec_photos.items(), key=lambda(k, v): v, reverse=True)
    rec_photos = [photo[0] for photo in rec_photos]
    res_photos = []
    for photo in rec_photos:
        res_photos.append(Photo.objects.get(id=photo))
    return res_photos