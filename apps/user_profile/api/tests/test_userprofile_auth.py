from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from rest_framework.status import HTTP_200_OK
from rest_framework.test import APITestCase


class UserProfileAuthTest(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            email="admin@example.com",
            first_name="test",
            last_name="test",
        )
        self.user.set_password('testpass1234')
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_auth_userprofile(self):
        url = reverse('auth')
        auth_data = {
            "email": "admin@example.com",
            "password": "testpass1234"
        }
        response = self.client.post(url, auth_data)
        self.assertEqual(response.status_code, HTTP_200_OK)
        expected_response_keys = {
            "id",
            "email",
            "first_name",
            "last_name",
            "auth_token"
        }
        self.assertEqual(expected_response_keys, set(response.data.keys()))
        self.assertTrue(get_user_model().objects.get(id=self.user.id).auth_token)

    def test_wrong_email_userprofile(self):
        url = reverse('auth')
        auth_data = {
            "email": "not_admin@example.com",
            "password": "testpass1234"
        }
        response = self.client.post(url, auth_data)
        self.assertContains(response, 'Wrong email or password.', status_code=400)
        with self.assertRaises(ObjectDoesNotExist):
            get_user_model().objects.get(id=self.user.id).auth_token
