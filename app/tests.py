from django.test import TestCase, Client
import nose.tools as nt
from models import *
import factory
import random
from factories import *
from search_algorithm import *
import unittest


class MyTestCase(TestCase):
    def test_unlogged_oauth_callback(self):
        c = Client()
        response = c.get('/oauth_callback/')

        self.assertContains(response, "Unknown Flickr account")

    def test_unlogged_get_photo(self):
        c = Client()
        response = c.get('/get_photo/', follow=True)
        print response.redirect_chain
        self.assertRedirects(response, "/?next=/get_photo/")

    def test_get_recommend_users(self):
        photos = PhotoFactory.create_batch(3)
        user = User.objects.create_user(
            username='test', password='pwd')
        me = FlickrUserFactory.create(nsid='1N01', user=user)
        like1 = LikingFactory(photo=photos[0], user=me)
        like2 = LikingFactory(photo=photos[1], user=me)

        flickruser = FlickrUserFactory(nsid='3N01')
        other_like1 = LikingFactory(photo=photos[1], user=flickruser)
        users=get_recommended_users(me, [like1, like2])
        print users[0].nsid
        self.assertEqual(users[0].nsid, flickruser.nsid)
