from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.test import APITestCase


class UserProfileCreateTest(APITestCase):
    def test_create_userprofile(self):
        url = reverse('register')
        data = {
            "email": "admin@example.com",
            "first_name": "test",
            "last_name": "test",
            "password": "testpass1234",
            "repeat_password": "testpass1234",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(get_user_model().objects.count(), 1)

    def test_wrong_email_userprofile(self):
        url = reverse('register')
        data = {
            "email": "admin@example",
            "first_name": "test",
            "last_name": "test",
            "password": "testpass1234",
            "repeat_password": "testpass1234",
        }
        response = self.client.post(url, data)
        expected_errors_keys_set = {
            'email'
        }
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(expected_errors_keys_set, set(response.data.keys()),)
