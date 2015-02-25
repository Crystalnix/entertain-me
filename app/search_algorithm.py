from time import time
from models import *
from utilities import *
import json
import datetime
__author__ = 'anmekin'


def update_user_likes(api, user_id, min_fave_date=0):
    user, created = User.objects.get_or_create(user_id=user_id)
    if user.last_get_faved and not min_fave_date:
        min_fave_date = user.last_get_faved
    photos = api.favorites.getList(user_id=user_id,
                                   min_fave_date=min_fave_date,
                                   extras='url_l, url_z, url_c')
    photos = json.loads(photos)
    photos = photos["photos"]["photo"]
    for photo in photos:
        url = choose_photo_URL(photo)
        _photo, created = Photo.objects.get_or_create(id=int(photo['id']),
                                                      owner=photo['owner'], url=url)
        dt = datetime.datetime.fromtimestamp(float(photo['date_faved']))
        liking, created = Liking.objects.get_or_create(photo=_photo, user=user, date_faved=dt)


def get_who_liked_photo(api, photo, per_page=10):
    list_users = []
    users = api.photos.getFavorites(photo_id=photo.id, per_page=per_page)
    users = json.loads(users)
    users = users['photo']['person']
    for user in users:
        _user, created = User.objects.get_or_create(user_id=user['nsid'])
        dt = datetime.datetime.fromtimestamp(float(user['favedate']))
        liking, created = Liking.objects.get_or_create(photo=photo, user=_user, date_faved=dt)
        list_users.append(_user)
    return list_users


def get_user_likes(api, user):
    photos = api.favorites.getList(user_id=user.user_id,
                                   extras='url_l, url_z, url_c', per_page=10)
    photos = json.loads(photos)
    photos = photos["photos"]["photo"]
    for photo in photos:
        url = choose_photo_URL(photo)
        _photo, created = Photo.objects.get_or_create(id=int(photo['id']),
                                                      owner=photo['owner'], url=url)
        dt = datetime.datetime.fromtimestamp(float(photo['date_faved']))
        liking, created = Liking.objects.get_or_create(photo=_photo, user=user, date_faved=dt)
    return photos


def get_recomended_users(api, my_id):
    # user, created = User.objects.get_or_create(user_id=my_id)
    rec_users = set()
    my_favs = Photo.objects.filter(user__user_id=my_id)
    for photo in my_favs:
        users = get_who_liked_photo(api, photo)
        rec_users.update(users)
    return rec_users


def get_recomended_photos(api, rec_users, my_id):
    rec_photos = {}
    my_favs = Photo.objects.filter(user__user_id=my_id)
    my_favs_ids = [x.id for x in my_favs]
    for user in rec_users:
        photos = get_user_likes(api, user)
        rec_photos = update_with_weight(rec_photos, photos, my_favs_ids)
    rec_photos = sorted(rec_photos.items(), key=lambda(k, v): v, reverse=True)
    rec_photos = [photo[0] for photo in rec_photos]
    res_photos = []
    for photo in rec_photos:
        res_photos.append(Photo.objects.get(id=photo))
    return res_photos