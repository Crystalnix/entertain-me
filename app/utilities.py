__author__ = 'anmekin'

def update_with_weight(d, l, my_favs):
    matches = 0
    for photo in l:
        if int(photo['id']) in my_favs:
            matches += 1
    weight_k = float(matches)/len(l)
    for photo in l:
        if photo['id'] in d:
            d[photo['id']] += weight_k
        else:
            d.update({photo['id']: weight_k})
    return d

def choose_photo_URL(photo):
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