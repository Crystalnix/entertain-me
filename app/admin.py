from django.contrib import admin
from django.shortcuts import render
from models import *
from django.contrib.admin.views.decorators import staff_member_required

admin.site.register(FlickrUser)
admin.site.register(Photo)
admin.site.register(Liking)
admin.site.register(Review)
# Register your models here.

@staff_member_required
def photo_info(request, id):
    photo = Photo.objects.get(id=id)
    return render(request, 'admin_photo.html', {'photo': photo})

@staff_member_required
def flickruser_info(request, pk):
    flickruser = FlickrUser.objects.get(pk=pk)
    return render(request, 'admin_flickruser.html', {'user': flickruser})