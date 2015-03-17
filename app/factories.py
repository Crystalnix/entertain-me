__author__ = 'anmekin'
from models import *
import factory
import random
from datetime import datetime
import unittest


class FlickrUserFactory(factory.DjangoModelFactory):
    class Meta:
        model = FlickrUser

    nsid = factory.Sequence(lambda n: '%sN01' % n)
    last_get_faved = 0
    user = None


class PhotoFactory(factory.DjangoModelFactory):
    class Meta:
        model = Photo
    id = factory.Sequence(lambda n: n)
    owner = factory.Sequence(lambda n: '%sN01' % n)
    url = None
    last_get_faved = 0

class LikingFactory(factory.DjangoModelFactory):
    class Meta:
        model = Liking
    user = factory.SubFactory(FlickrUserFactory)
    photo = factory.SubFactory(PhotoFactory)
    date_faved = datetime.now()

class ReviewFactory(factory.DjangoModelFactory):
    class Meta:
        model = Review

    user = factory.SubFactory(FlickrUserFactory)
    photo = factory.SubFactory(PhotoFactory)
    date_review = datetime.now()

class WeightFactory(factory.DjangoModelFactory):
    class Meta:
        model = Weight

    against = factory.SubFactory(FlickrUserFactory)
    to = factory.SubFactory(FlickrUserFactory)
    weight = factory.Sequence(lambda n: 1/n)

class MTMFlickrUserFactory(FlickrUserFactory):
    favorited = factory.RelatedFactory(LikingFactory, 'user')
    reviewed = factory.RelatedFactory(ReviewFactory, 'user')