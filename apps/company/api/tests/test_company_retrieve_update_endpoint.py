from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED
from rest_framework.test import APITestCase

from apps.company.models import Company


class CompanyRetrieveUpdateAPIViewTestCase(APITestCase):
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
            name="Company name",
            address="Company address",
            owner=self.user,
        )

    def tearDown(self):
        self.user.delete()
        self.company.delete()

    def test_retrieve_company(self):
        response = self.client.get(reverse('company', kwargs={'pk': self.company.id}))
        self.assertEqual(response.status_code, HTTP_200_OK)
        expected_response_keys = {
            'id',
            'name',
            'address'
        }
        self.assertEqual(set(response.data.keys()), expected_response_keys)

    def test_update_put_company(self):
        update_company_data = {
            "name": "Company test name",
            "address": "Company test address",
        }
        response = self.client.put(reverse('company', kwargs={'pk': self.company.id}), update_company_data)
        self.assertEqual(response.status_code, HTTP_200_OK)
        expected_response_keys = {
            'id',
            'name',
            'address'
        }
        self.assertEqual(set(response.data.keys()), expected_response_keys)
        self.assertEqual(Company.objects.get(pk=self.company.id).name, update_company_data['name'])
        self.assertEqual(Company.objects.get(pk=self.company.id).address, update_company_data['address'])

    def test_unauthorized_user_update_patch_company(self):
        self.client.credentials()
        update_company_data = {
            "name": "Company test name"
        }
        response = self.client.patch(reverse('company', kwargs={'pk': self.company.id}), update_company_data)
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)
