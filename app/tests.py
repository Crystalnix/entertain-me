from django.test import TestCase, Client
import nose.tools as nt
from models import *
import factory
import random
from factories import *
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
