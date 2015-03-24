from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


# Create your models here.

class Photo(models.Model):
    """
    Model for Flickr photos:
      |  id - id photo on Flickr;
      |  owner - owner's nsid;
      |  last_get_faved - datetime of last calling update_photo() in Unix timestamp
    """
    id = models.BigIntegerField(primary_key=True)
    owner = models.CharField(max_length=32)
    url = models.URLField(null=True)
    last_get_faved = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id)


class FlickrUser(models.Model):
    """
    Model for Flickr users:
      |  id - nsid on Flickr;
      |  owner - owner's nsid;
      |  last_get_faved - datetime of last calling update_flickr_user() in Unix timestamp
      |  user - related User model from this application
      |  favorited - M2M relationship with photos which he liked
      |  reviewed - M2M relationship with photos which he already seen
    """
    nsid = models.CharField(max_length=32)
    favorited = models.ManyToManyField(Photo, through='Liking', related_name='favorited')
    last_get_faved = models.IntegerField(default=0)
    user = models.OneToOneField(User, null=True)
    reviewed = models.ManyToManyField(Photo, through='Review', related_name='reviewed')

    def __str__(self):
        return str(self.nsid)


class Liking(models.Model):
    """
    Model which keep date/time of user's likes:
      |  date_faved - datetime in readable Date/time
    """
    photo = models.ForeignKey(Photo)
    user = models.ForeignKey(FlickrUser)
    date_faved = models.DateTimeField(null=True)

    def __str__(self):
        return "%s -> %s" % (self.user, self.photo.id)


class Review(models.Model):
    """
    Model which keep date/time of user's viewed photos:
      |  date_view - datetime in readable Date/time
    """
    photo = models.ForeignKey(Photo)
    user = models.ForeignKey(FlickrUser)
    date_review = models.DateTimeField(default=datetime.now, blank=True)

    def __str__(self):
        return "%s -> %s" % (self.user, self.photo.id)


class Weight(models.Model):
    """
    Model which keep ratio of interesting from AGAINST user to TO user:
      |  weight - ratio in float format
    """
    against = models.ForeignKey(FlickrUser, related_name='against_weight')
    to = models.ForeignKey(FlickrUser, related_name='to_weight')
    weight = models.FloatField(default=0)

    def __str__(self):
        return "%s -> %s = %d" % (self.against, self.to, self.weight)