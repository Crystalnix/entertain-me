__author__ = 'anmekin'
from models import *
import factory
import random
from datetime import datetime
import unittest


class FlickrUserFactory(factory.Factory):
    class Meta:
        model = FlickrUser

    nsid = factory.Sequence(lambda n: '%sN01' % n)
    last_get_faved = 0
    user = None


class PhotoFactory(factory.Factory):
    class Meta:
        model = Photo
    id = factory.Sequence(lambda n: n)
    owner = factory.Sequence(lambda n: '%sN01' % n)
    url = None
    last_get_faved = 0

class LikingFactory(factory.Factory):
    class Meta:
        model = Liking
    user = factory.SubFactory(FlickrUserFactory)
    photo = factory.SubFactory(PhotoFactory)
    date_faved = datetime.now()

class ReviewFactory(factory.Factory):
    class Meta:
        model = Review

    user = factory.SubFactory(FlickrUserFactory)
    photo = factory.SubFactory(PhotoFactory)
    date_review = datetime.now()

class MTMFlickrUserFactory(FlickrUserFactory):
    favorited = factory.RelatedFactory(LikingFactory, 'flickruser')
    reviewed = factory.RelatedFactory(ReviewFactory, 'flickruser')