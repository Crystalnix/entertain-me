from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


# Create your models here.

class Photo(models.Model):
    id = models.BigIntegerField(primary_key=True)
    owner = models.CharField(max_length=32)
    url = models.URLField(null=True)
    last_get_faved = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id)


class FlickrUser(models.Model):
    nsid = models.CharField(max_length=32)
    favorited = models.ManyToManyField(Photo, through='Liking', related_name='favorited')
    last_get_faved = models.IntegerField(default=0)
    user = models.OneToOneField(User, null=True)
    reviewed = models.ManyToManyField(Photo, through='Review', related_name='reviewed')

    def __str__(self):
        return str(self.nsid)


class Liking(models.Model):
    photo = models.ForeignKey(Photo)
    user = models.ForeignKey(FlickrUser)
    date_faved = models.DateTimeField(null=True)

    def __str__(self):
        return "%s -> %s" % (self.user, self.photo.id)


class Review(models.Model):
    photo = models.ForeignKey(Photo)
    user = models.ForeignKey(FlickrUser)
    date_review = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return "%s -> %s" % (self.user, self.photo.id)


class Weight(models.Model):
    against = models.ForeignKey(FlickrUser, related_name='against_weight')
    to = models.ForeignKey(FlickrUser, related_name='to_weight')
    weight = models.FloatField(default=0)

    def __str__(self):
        return "%s -> %s = %d" % (self.against, self.to, self.weight)