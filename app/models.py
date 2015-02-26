from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Photo(models.Model):
    id = models.BigIntegerField(primary_key=True)
    owner = models.CharField(max_length=32)
    url = models.URLField(null=True)
    last_get_faved = models.IntegerField(default=0)

class FlickrUser(models.Model):
    user_id = models.CharField(max_length=32)
    favorited = models.ManyToManyField(Photo, through='Liking')
    last_get_faved = models.IntegerField(default=0)
    # user = models.OneToOneField(User) this field will brake everything, add him later

class Liking(models.Model):
    photo = models.ForeignKey(Photo)
    user = models.ForeignKey(FlickrUser)
    date_faved = models.DateTimeField()


