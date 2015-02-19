from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.conf import settings
import flickrapi

def auth(request):
    api_key = u'345f75b44303f45dd5356ee57b54df81'
    api_secret = u'90aef24a6b3558ed'
    f = flickrapi.FlickrAPI(api_key, api_secret)
    #flickr = flickrapi.FlickrAPI(settings.api_key, settings.api_secret)
    #flickr.get_request_token(oauth_callback='oauth_callback')
    url = f.web_login_url(perms='read')
    return HttpResponseRedirect(url)

    #return HttpResponse('ok')

def test(request):

    flickr = flickrapi.FlickrAPI(settings.api_key, settings.api_secret)
    sets = flickr.photosets.getList(user_id='73509078@N00')
    title = sets['photosets']['photoset'][0]['title']['_content']

    print('First set title: %s' % title)
    return HttpResponse('200')
# Create your views here.

def oauth_callback(request):
    frob = request.GET['frob']
    print frob
    return HttpResponse(frob)

def my_auth(request):
    def calcSig(secret,params):
        import hashlib
        l = params.keys()
        l.sort()
        hash = ''
        for key in l:
          hash += str(key) + params[key].encode('utf-8')
        hash = secret + hash
        api_sig = hashlib.md5(hash).hexdigest()
        return api_sig
    api_key = u'345f75b44303f45dd5356ee57b54df81'
    api_secret = u'90aef24a6b3558ed'
    perms = 'write'
    api_sig = calcSig(api_secret,{'api_key': api_key, 'perms': perms})
    login_url = "http://flickr.com/services/auth/?api_key=%s&perms=%s&api_sig=%s" % (api_key, perms, api_sig)
    return HttpResponse(login_url)