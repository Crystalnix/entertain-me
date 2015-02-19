from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import logout as auth_logout
#from social_auth.models import UserSocialAuth

def auth(request):
#    print UserSocialAuth.objects.filter(provider='flickr').get(id='1').tokens
    return render(request, 'auth.html')


def home(request):
    print request.user.username
    return render(request, 'index.html')

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')

