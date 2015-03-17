from django.contrib import admin
from django.shortcuts import render
from models import *
from django.contrib.admin.views.decorators import staff_member_required


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'show_url', 'last_get_faved')

    def show_url(self, obj):
        return '<a href="%s">%s</a>' % (obj.url, obj.url)
    show_url.allow_tags = True

class FlickrUserAdmin(admin.ModelAdmin):
    list_display = ('nsid',
                    'show_user_username',
                    'show_user_first_name',
                    'show_user_last_name',
                    'show_user_email',
                    'last_get_faved')

    def show_user_username(self, obj):
        if obj.user:
            return 'Username: %s' % (obj.user.username)
        else:
            return ''

    def show_user_first_name(self, obj):
        if obj.user:
            return 'First name: %s' % (obj.user.first_name)
        else:
            return ''

    def show_user_last_name(self, obj):
        if obj.user:
            return 'last_name: %s' % (obj.user.last_name)
        else:
            return ''

    def show_user_email(self, obj):
        if obj.user:
            return 'email: %s' % (obj.user.email)
        else:
            return ''


admin.site.register(FlickrUser, FlickrUserAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Liking)
admin.site.register(Review)
admin.site.register(Weight)
