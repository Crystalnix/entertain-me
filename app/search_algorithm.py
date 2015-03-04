__author__ = 'anmekin'
from models import *
from utilities import *
import datetime


def update_user_likes(api, user_id, min_fave_date=0):
    user, created = FlickrUser.objects.get_or_create(nsid=user_id)
    if user.last_get_faved and not min_fave_date:
        min_fave_date = user.last_get_faved
    photos = api.favorites.getList(user_id=user_id,
                                   min_fave_date=min_fave_date,
                                   extras='url_l, url_z, url_c')
    photos = photos["photos"]["photo"]
    for photo in photos:
        url = choose_photo_URL(photo)
        _photo, created = Photo.objects.get_or_create(id=int(photo['id']),
                                                      owner=photo['owner'], url=url)
        dt = datetime.datetime.fromtimestamp(float(photo['date_faved']))
        liking, created = Liking.objects.get_or_create(photo=_photo, user=user, date_faved=dt)


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