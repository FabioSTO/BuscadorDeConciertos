import json
from unittest import mock
from django.test import Client, TestCase
from django.urls import reverse

from BuscadorConciertos.models import Artist
from . import views

# Create your tests here.

class SpotiTestCase(TestCase):
    
    def setUp(self):
        self.client = Client()

    @mock.patch('requests.post')
    def test_get_token(self, mock_post):
        mock_response = mock.Mock()
        mock_response.json.return_value = {'access_token': 'test_token'}
        mock_post.return_value = mock_response

        code = 'test_code'
        token = views.get_Spotoken(code)

        self.assertAlmostEquals(token, 'test_token')

    @mock.patch('requests.get')
    def test_get_user_id(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = {
            'display_name': 'test_user',
            'images': [{'url': 'test_image_url'}]
        }
        mock_get.return_value = mock_response

        username, userpic = views.get_user_id(None)
        self.assertEquals(username, 'test_user')
        self.assertEquals(userpic, 'test_image_url')

    @mock.patch('requests.get')
    def test_get_top_artists(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = {
            'items': [
                {'name': 'artist1'},
                {'name': 'artist2'},
                {'name': 'artist3'}
            ]
        }
        mock_get.return_value = mock_response

        response = views.get_top_artists(None)

        self.assertEqual(response.status_code, 204)

    @mock.patch('requests.get')
    def test_get_playlists(self, mock_get):
        mock_response = mock.Mock()
        mock_response.json.return_value = {
            'items': [
                {'name': 'playlist1', 'id': '1'},
                {'name': 'playlist2', 'id': '2'},
                {'name': 'playlist3', 'id': '3'}
            ]
        }
        mock_get.return_value = mock_response

        response = views.get_playlists(None)
        playlists = json.loads(response.content)
        expected_playlists = ['playlist1', 'playlist2', 'playlist3']
        
        self.assertEqual(playlists, expected_playlists)
    