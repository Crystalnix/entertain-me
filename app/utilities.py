"""
Module with useful functions
"""
__author__ = 'anmekin'
from models import Photo, Weight


def update_weight(user, user_favs, rec_user, rec_user_favs):
    """
    Calculate weight between two users on base of photos which they liked
    """
    counter = 0
    for photo in user_favs:
        if photo in rec_user_favs:
            counter += 1
    weight, created = Weight.objects.get_or_create(against=user, to=rec_user)
    weight.weight = float(counter)/len(rec_user_favs)
    weight.save()


def choose_photo_URL(photo):
    """
    Choose most suitable url of photo or None if photo too small.
    """
    try:
        url = photo['url_l']
    except KeyError:
        try:
            url = photo['url_z']
        except KeyError:
            try:
                url = photo['url_c']
            except KeyError:
                return None
    return url