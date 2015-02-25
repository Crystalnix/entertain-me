from django.db import models
from time import time

# Create your models here.
class Photo(models.Model):
    id = models.BigIntegerField(primary_key=True)
    owner = models.CharField(max_length=32)
    url = models.URLField()




class User(models.Model):
    user_id = models.CharField(max_length=32)
    favorited = models.ManyToManyField(Photo, through='Liking')
    last_get_faved = models.IntegerField(default=int(time()))



class Liking(models.Model):
    photo = models.ForeignKey(Photo)
    user = models.ForeignKey(User)
    date_faved = models.DateTimeField()
