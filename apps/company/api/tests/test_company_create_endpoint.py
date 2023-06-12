from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.status import HTTP_201_CREATED, HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN
from rest_framework.test import APITestCase

from apps.company.models import Company


class CompanyCreateAPIViewTestCase(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            email="admin@example.com",
            first_name="test",
            last_name="test",
        )
        self.user.set_password('testpass1234')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        self.company = Company.objects.create(
            name="New Company test",
            address="New Company address test",
            owner=self.user
        )

    def tearDown(self):
        self.user.delete()
        if self.company.id:
            self.company.delete()

    def test_create_company(self):
        self.company.delete()
        url = reverse('companies')
        create_company_data = {
            "name": "Company test",
            "address": "Company address test"
        }
        response = self.client.post(url, create_company_data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(Company.objects.count(), 1)
        self.assertEqual(response.data['address'], create_company_data['address'])

    def test_unauthorized_user_create_company(self):
        self.client.credentials()
        url = reverse('companies')
        create_company_data = {
            "name": "Company test",
            "address": "Company address test"
        }
        response = self.client.post(url, create_company_data)
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)

    def test_owner_company_create_company(self):
        url = reverse('companies')
        create_company_data = {
            "name": "Company test",
            "address": "Company address test"
        }
        response = self.client.post(url, create_company_data)
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
