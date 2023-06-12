from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from rest_framework.test import APITestCase

from apps.company.models import Company
from apps.office.models import Office
from apps.vehicle.models import Vehicle


class WorkerRetrieveUpdateDestroyAPIViewTestCase(APITestCase):
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
        self.worker = get_user_model().objects.create(
            email="worker@example.com",
            first_name="test",
            last_name="test",
        )
        self.worker.set_password('testpass1234')
        self.office = Office.objects.create(
            name="Office name",
            address="Office address",
            country="Office country",
            city="Office city",
            region="Office region",
            company=self.company
        )
        self.vehicle = Vehicle.objects.create(
            name="Vehicle name",
            licence_plate="Vehicle licence plate",
            model="Vehicle model",
            year_of_manufacture=2014,
            company=self.company,
            office=self.office
        )
        self.company.workers.add(self.worker)
        self.office.workers.add(self.worker)
        self.vehicle.drivers.add(self.worker)
        self.new_office = Office.objects.create(
            name="Another office name",
            address="Office address",
            country="Office country",
            city="Office city",
            region="Office region",
            company=self.company
        )

    def tearDown(self):
        self.user.delete()
        self.company.delete()
        self.office.delete()
        self.new_office.delete()
        self.vehicle.delete()
        self.worker.delete()

    def test_retrieve_worker(self):
        response = self.client.get(reverse('worker', kwargs={'pk': self.worker.id}))
        self.assertEqual(response.status_code, HTTP_200_OK)
        expected_response_keys = {
            'id',
            'email',
            'first_name',
            'last_name',
            'office',
            'vehicle_set'
        }
        self.assertEqual(set(response.data.keys()), expected_response_keys)

    def test_update_put_worker(self):
        update_worker_data = {
            "email": "not_worker@example.com",
            "first_name": "Test123",
            "last_name": "Test123",
            "password": "testpassword1234",
            "repeat_password": "testpassword1234",
        }
        response = self.client.put(reverse('worker', kwargs={'pk': self.worker.id}), update_worker_data)
        self.assertEqual(response.status_code, HTTP_200_OK)
        expected_response_keys = {
            'id',
            'email',
            'first_name',
            'last_name',
            'office',
            'vehicle_set'
        }
        self.assertEqual(set(response.data.keys()), expected_response_keys)
        self.assertTrue(get_user_model().objects.get(pk=self.worker.id).check_password(update_worker_data['password']))
        self.assertNotEqual(get_user_model().objects.get(pk=self.worker.id).email, update_worker_data['email'])

    def test_update_patch_diff_passwords_worker(self):
        update_worker_password_data = {
            "password": "testpassword1234",
            "repeat_password": "pass",
        }
        response = self.client.patch(reverse('worker', kwargs={'pk': self.worker.id}), update_worker_password_data)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        expected_errors_keys_set = {
            'non_field_errors'
        }
        self.assertEqual(set(response.data.keys()), expected_errors_keys_set)
        self.assertFalse(get_user_model().objects.get(pk=self.worker.id).check_password(update_worker_password_data['password']))

    def test_destroy_worker(self):
        response = self.client.delete(reverse('worker', kwargs={'pk': self.worker.id}))
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
        self.assertFalse(get_user_model().objects.filter(pk=self.worker.id).exists())

    def test_office_none_and_vehicle_empty_set(self):
        update_worker_office_and_vehicle_set_data = {
            "office": None,
            "vehicle_set": []
        }
        response = self.client.patch(reverse('worker', kwargs={'pk': self.worker.id}),
                                     update_worker_office_and_vehicle_set_data)
        self.assertEqual(response.status_code, HTTP_200_OK)
        expected_response_keys = {
            'id',
            'email',
            'first_name',
            'last_name',
            'office',
            'vehicle_set'
        }
        self.assertEqual(set(response.data.keys()), expected_response_keys)
        self.assertIsNone(get_user_model().objects.get(pk=self.worker.id).office)
        self.assertFalse(get_user_model().objects.get(pk=self.worker.id).vehicle_set.all())

    def test_vehicle_empty_set(self):
        update_vehicle_set_data = {
            "vehicle_set": [],
        }
        response = self.client.patch(reverse('worker', kwargs={'pk': self.worker.id}), update_vehicle_set_data)
        self.assertEqual(response.status_code, HTTP_200_OK)
        expected_response_keys = {
            'id',
            'email',
            'first_name',
            'last_name',
            'office',
            'vehicle_set'
        }
        self.assertEqual(set(response.data.keys()), expected_response_keys)
        self.assertIsNotNone(get_user_model().objects.get(pk=self.worker.id).office)
        self.assertFalse(get_user_model().objects.get(pk=self.worker.id).vehicle_set.all())

    def test_vehicle_not_belong_to_office(self):
        self.vehicle.office = None
        self.worker.vehicle_set.set([])
        update_vehicle_set_data = {
            "vehicle_set": [self.vehicle.id]
        }
        response = self.client.patch(reverse('worker', kwargs={'pk': self.worker.id}), update_vehicle_set_data)
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        expected_errors_keys_set = {
            'non_field_errors'
        }
        self.assertEqual(set(response.data.keys()), expected_errors_keys_set)
        self.assertFalse(get_user_model().objects.get(pk=self.worker.id).vehicle_set.all())

    def test_other_office_remove_existing_vehicle_set(self):
        update_worker_office_data = {
            'office': self.new_office.id
        }
        response = self.client.patch(reverse('worker', kwargs={'pk': self.worker.id}), update_worker_office_data)
        self.assertEqual(response.status_code, HTTP_200_OK)
        expected_response_keys = {
            'id',
            'email',
            'first_name',
            'last_name',
            'office',
            'vehicle_set'
        }
        self.assertEqual(set(response.data.keys()), expected_response_keys)
        self.assertEqual(get_user_model().objects.get(pk=self.worker.id).office, self.new_office)
        self.assertFalse(get_user_model().objects.get(pk=self.worker.id).vehicle_set.all())
