from django.test import TestCase, Client
import nose.tools as nt
from models import *
import factory
import random
from factories import *
from search_algorithm import *
import unittest
from tasks import *
from mocks import *
import mock


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


class FlickTasksCase(TestCase):

    def test_update_photo(self):
        photo = Photo.objects.create(id=1, owner='01N01')
        with mock.patch('flickrapi.FlickrAPI') as perm_mock:
            instance = perm_mock.return_value
            instance.photos.getFavorites.return_value = get_fake_users()
            update_photo()
        self.assertTrue(FlickrUser.objects.first())


    def test_wrong_response_update_photo(self):
        photo = Photo.objects.create(id=1, owner='01N01')
        with mock.patch('flickrapi.FlickrAPI') as perm_mock:
            instance = perm_mock.return_value
            instance.photos.getFavorites.return_value = bad_request_users()
        self.assertRaisesMessage(RuntimeError, "Wrong Flickr response", update_photo)

    def test_empty_photos_update_photo(self):
        with mock.patch('flickrapi.FlickrAPI') as my_mock:
            instance = my_mock.return_value
            instance.photos.getFavorites.return_value = get_fake_users()
        self.assertRaisesMessage(RuntimeError, "Empty photos list", update_photo)

    def test_update_user(self):
        user = User.objects.create_user(
            username='test', password='pwd')
        me = FlickrUser.objects.create(nsid='1N01', user=user, last_get_faved=1)
        other = FlickrUser.objects.create(nsid='2N01')
        photo1 = Photo.objects.create(id=1, owner='01N01')
        photo2 = Photo.objects.create(id=2, owner='01N01')
        photo3 = Photo.objects.create(id=3, owner='01N01')
        like1 = Liking.objects.create(photo=photo1, user=me)
        like2 = Liking.objects.create(photo=photo2, user=me)
        like3 = Liking.objects.create(photo=photo2, user=other)
        like4 = Liking.objects.create(photo=photo3, user=other)
        with mock.patch('flickrapi.FlickrAPI') as my_mock:
            instance = my_mock.return_value
            instance.favorites.getList.return_value = get_fake_photos()
            update_flickr_user()
        photos = Photo.objects.all()
        self.assertEqual(len(photos), 4)
        self.assertTrue(Liking.objects.filter(user=other, photo=Photo.objects.last()))

    def test_wrong_response_update_user(self):
        user = User.objects.create_user(
            username='test', password='pwd')
        me = FlickrUser.objects.create(nsid='1N01', user=user, last_get_faved=1)
        with mock.patch('flickrapi.FlickrAPI') as my_mock:
            instance = my_mock.return_value
            instance.favorites.getList.return_value = get_fake_photos()
        with self.assertRaisesMessage(RuntimeError, "Wrong Flickr response"):
            update_flickr_user(flickruser=me)

    def test_empty_users_update_user(self):
        with mock.patch('flickrapi.FlickrAPI') as my_mock:
            instance = my_mock.return_value
            instance.favorites.getList.return_value = get_fake_photos()
        with self.assertRaisesMessage(RuntimeError, "Empty flickrUsers list"):
            update_flickr_user()


    # def test_get_recommend_users(self):
    #     photos = PhotoFactory.create_batch(3)
    #     user = User.objects.create_user(
    #         username='test', password='pwd')
    #     me = FlickrUserFactory.create(nsid='1N01', user=user)
    #     like1 = LikingFactory(photo=photos[0], user=me)
    #     like2 = LikingFactory(photo=photos[1], user=me)
    #
    #     flickruser = FlickrUserFactory(nsid='3N01')
    #     other_like1 = LikingFactory(photo=photos[1], user=flickruser)
    #     users=get_recommended_users(me, [like1, like2])
    #     print users[0].nsid
    #     self.assertEqual(users[0].nsid, flickruser.nsid)
