from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED
from rest_framework.test import APITestCase


class UserProfileAuthTest(APITestCase):
    def setUp(self):
        user = get_user_model().objects.create(
            email="admin@example.com",
            first_name="test",
            last_name="test",
        )
        user.set_password('testpass1234')
        user.save()
        self.user = get_user_model().objects.get(id=user.id)
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

    def tearDown(self):
        self.user.delete()

    def test_get_userprofile_profile(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, HTTP_200_OK)
        expected_response_keys = {
            'id',
            'email',
            'first_name',
            'last_name'
        }
        self.assertEqual(expected_response_keys, set(response.data.keys()))

    def test_unauthorized_userprofile_profile(self):
        self.client.credentials()
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)
        expected_errors_keys_set = {
            'detail'
        }
        self.assertEqual(expected_errors_keys_set, set(response.data.keys()))
