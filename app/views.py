from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.conf import settings


def auth(request):
    return render(request, 'auth.html')


def home(request):
    return render(request, 'index.html')



