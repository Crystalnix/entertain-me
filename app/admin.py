from django.contrib import admin
from django.shortcuts import render
from models import *
from django.contrib.admin.views.decorators import staff_member_required

class WeightAdmin(admin.ModelAdmin):
    list_display = ('against', 'to', 'weight')

class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'show_url', 'last_get_faved')

    def show_url(self, obj):
        return '<a href="%s">%s</a>' % (obj.url, obj.url)
    show_url.allow_tags = True

class FlickrUserAdmin(admin.ModelAdmin):
    list_display = ('nsid',
                    'username',
                    'first_name',
                    'last_name',
                    'email',
                    'last_get_faved')

    def username(self, obj):
        if obj.user:
            return obj.user.username
        else:
            return ''
    username.admin_order_field = 'user__username'

    def first_name(self, obj):
        if obj.user:
            return obj.user.first_name
        else:
            return ''
    first_name.admin_order_field = 'user__first_name'

    def last_name(self, obj):
        if obj.user:
            return obj.user.last_name
        else:
            return ''
    last_name.admin_order_field = '-user__last_name'

    def email(self, obj):
        if obj.user:
            return obj.user.email
        else:
            return ''
    email.admin_order_field = 'user__email'

admin.site.register(FlickrUser, FlickrUserAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Liking)
admin.site.register(Review)
admin.site.register(Weight, WeightAdmin)
