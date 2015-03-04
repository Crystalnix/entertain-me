__author__ = 'anmekin'

def update_with_weight(rec_photos, photos, my_favs, reviewed):

    unseen_photos = list(photos - set(my_favs) - set(reviewed))
    if not unseen_photos:          # some photos can be empty
        return rec_photos
    matches = 0
    for photo in photos:
        if photo in my_favs:
            matches += 1
    weight_k = float(matches)/len(photos)
    for photo in unseen_photos:
        if photo.id in rec_photos:
            rec_photos[photo.id] += weight_k
        else:
            rec_photos.update({photo.id: weight_k})
    return rec_photos


# def update_with_weight(rec_photos, photos, my_favs):
#     if not photos:          # some photos can be empty
#         return rec_photos
#     matches = 0
#     for photo in photos:
#         if int(photo.id) in my_favs:
#             matches += 1
#     weight_k = float(matches)/len(photos)
#     for photo in photos:
#         if photo.id in rec_photos:
#             rec_photos[photo['id']] += weight_k
#         else:
#             rec_photos.update({photo['id']: weight_k})
#     return rec_photos

def choose_photo_URL(photo): # has_key
    try:                            # ugly construction
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