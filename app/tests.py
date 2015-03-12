from django.test import TestCase, Client
from factories import *
import search_algorithm as sa
import json
from tasks import *
from mocks import *
import mock


class UnloggedTestCase(TestCase):

    def test_unlogged_oauth_callback(self):
        c = Client()
        response = c.get('/oauth_callback/')

        self.assertContains(response, "Unknown Flickr account")

    def test_unlogged_get_photo(self):
        c = Client()
        response = c.get('/', follow=True)
        print response.redirect_chain
        self.assertRedirects(response, "auth/?next=/")


class FlickrTasksCase(TestCase):

    def test_update_photo(self):
        photo = PhotoFactory(id=1, owner='01N01')
        with mock.patch('flickrapi.FlickrAPI') as perm_mock:
            instance = perm_mock.return_value
            instance.photos.getFavorites.return_value = get_fake_users()
            update_photo()
        self.assertTrue(FlickrUser.objects.first())


    def test_wrong_response_update_photo(self):
        photo = PhotoFactory(id=1, owner='01N01')
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
        me = FlickrUserFactory(nsid='1N01', user=user, last_get_faved=1)
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
        me = FlickrUserFactory(nsid='1N01', user=user, last_get_faved=1)
        with mock.patch('flickrapi.FlickrAPI') as my_mock:
            instance = my_mock.return_value
            instance.favorites.getList.return_value = bad_request_photos()
            with self.assertRaisesMessage(RuntimeError, "Wrong Flickr response"):
                update_flickr_user(flickruser=me)

    def test_empty_users_update_user(self):
        with mock.patch('flickrapi.FlickrAPI') as my_mock:
            instance = my_mock.return_value
            instance.favorites.getList.return_value = get_fake_photos()
        with self.assertRaisesMessage(RuntimeError, "Empty flickrUsers list"):
            update_flickr_user()


class SearchAlgorithmCase(TestCase):

    def setUp(self):
        self.photos = PhotoFactory.create_batch(6)
        user = User.objects.create_user(username='test', password='pwd')
        self.me = FlickrUserFactory.create(nsid='1N01', user=user)
        like1 = LikingFactory(photo=self.photos[0], user=self.me)
        like2 = LikingFactory(photo=self.photos[1], user=self.me)
        review = ReviewFactory(photo=self.photos[3], user=self.me)

        self.flickruser1 = FlickrUserFactory(nsid='4N01')        # weight 0,33
        fu1_like1 = LikingFactory(photo=self.photos[1], user=self.flickruser1)
        fu1_like2 = LikingFactory(photo=self.photos[2], user=self.flickruser1)
        fu1_like3 = LikingFactory(photo=self.photos[3], user=self.flickruser1)

        self.flickruser2 = FlickrUserFactory(nsid='5N01')        # weight 0,5
        fu2_like1 = LikingFactory(photo=self.photos[0], user=self.flickruser2)
        fu2_like2 = LikingFactory(photo=self.photos[1], user=self.flickruser2)
        fu2_like3 = LikingFactory(photo=self.photos[3], user=self.flickruser2)
        fu2_like4 = LikingFactory(photo=self.photos[4], user=self.flickruser2)


    def test_get_recommended_users(self):

        my_favs = Photo.objects.filter(favorited=self.me)
        users = sa.get_recommended_users(self.me, my_favs)
        self.assertEqual(len(users), 2)


    def test_update_with_weight(self):

        photos = Photo.objects.filter(favorited=self.flickruser2)
        my_favs = Photo.objects.filter(favorited=self.me)
        reviewed = Photo.objects.filter(reviewed=self.me)
        rec_photos = update_with_weight({}, set(photos), my_favs, reviewed)
        exp_best_photo_id = self.photos[4].id
        self.assertEqual(rec_photos[exp_best_photo_id], 0.5)


    def test_get_recommended_photos(self):
        my_favs = Photo.objects.filter(favorited=self.me)
        reviewed = Photo.objects.filter(reviewed=self.me)
        rec_photos = sa.get_recommended_photos([self.flickruser1, self.flickruser2], my_favs, reviewed)
        self.assertEqual(rec_photos[0], self.photos[4])


class ViewTestCase(TestCase):

    def test_get_photo_empty_photos(self):
        user = User.objects.create_user(username='test', password='pwd')
        me = FlickrUserFactory.create(nsid='1N01', user=user)
        c = Client()
        c.login(username='test', password='pwd')
        with mock.patch('app.search_algorithm') as perm_mock:
            perm_mock.get_recommended_users.return_value = []
            perm_mock.get_recommended_photos.return_value = []
        response = c.get('/')
        self.assertContains(response, "Photos not found.")


    def test_get_photo(self):
        user = User.objects.create_user(username='test', password='pwd')
        me = FlickrUserFactory.create(nsid='1N01', user=user)
        photo = PhotoFactory(id=1, owner='01N01')
        c = Client()
        c.login(username='test', password='pwd')
        with mock.patch('app.search_algorithm.get_recommended_photos') as perm_mock:
            perm_mock.return_value = [photo]
            response = c.get('/')
        reviewed = Photo.objects.filter(reviewed=me)
        self.assertEqual(len(reviewed), 1)



    def test_get_photo_ajax(self):
        user = User.objects.create_user(username='test', password='pwd')
        me = FlickrUserFactory.create(nsid='1N01', user=user)
        photo = PhotoFactory(id=1, owner='01N01', url='http://google.com')
        c = Client()
        c.login(username='test', password='pwd')
        with mock.patch('app.search_algorithm.get_recommended_photos') as perm_mock:
            perm_mock.return_value = [photo]
            response = c.get('/', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        response = json.loads(response.content)
        reviewed = Photo.objects.filter(reviewed=me)
        self.assertEqual(response['id'], 1)
