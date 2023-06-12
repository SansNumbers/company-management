from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.status import HTTP_201_CREATED, HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN
from rest_framework.test import APITestCase

from apps.company.models import Company


class WorkerListCreateAPIViewTestCase(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            email="admin@example.com",
            first_name="test",
            last_name="test",
        )
        self.user.set_password('testpass1234')
        self.token = Token.objects.create(user=self.user)
        self.company = Company.objects.create(
            name="Company name",
            address="Company address",
            owner=self.user,
        )

    def tearDown(self):
        self.user.delete()
        if self.company.id:
            self.company.delete()

    def test_create_worker(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        url = reverse('workers')
        create_worker_data = {
            "email": "worker@example.com",
            "first_name": "test",
            "last_name": "test",
            "password": "testpass1234",
            "repeat_password": "testpass1234",
        }
        response = self.client.post(url, create_worker_data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(Company.objects.first().workers.count(), 1)
        expected_response_keys = {
            "id",
            "first_name",
            "last_name",
            "email",
        }
        self.assertEqual(expected_response_keys, set(response.data.keys()))

    def test_unauthorized_user_create_worker(self):
        url = reverse('workers')
        create_worker_data = {
            "email": "worker@example.com",
            "first_name": "test",
            "last_name": "test",
            "password": "testpass1234",
            "repeat_password": "testpass1234",
        }
        response = self.client.post(url, create_worker_data)
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)

    def test_no_company_user_create_worker(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        self.company.delete()
        url = reverse('workers')
        create_worker_data = {
            "email": "worker@example.com",
            "first_name": "test",
            "last_name": "test",
            "password": "testpass1234",
            "repeat_password": "testpass1234",
        }
        response = self.client.post(url, create_worker_data)
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
