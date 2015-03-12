from django.contrib import admin
from django.shortcuts import render
from models import *
from django.contrib.admin.views.decorators import staff_member_required

admin.site.register(FlickrUser)
admin.site.register(Photo)
admin.site.register(Liking)
admin.site.register(Review)
# Register your models here.
