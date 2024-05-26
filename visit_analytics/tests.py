from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from visit_analytics.models import Worker, Unit, Visit
import json


class GetUnitsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('list_of_units')
        self.worker = Worker.objects.create(name='Wali', phone_number='1234567890')
        self.unit_one = Unit.objects.create(name='Unit 1', worker=self.worker)
        self.unit_two = Unit.objects.create(name='Unit 2', worker=self.worker)

    def test_worker_does_not_exist(self):
        response = self.client.post(self.url, {'number': '0987654321'})
        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(response.content, {'message': 'worker with phone number does not exist'})

    def test_worker_has_no_units(self):
        new_worker = Worker.objects.create(name='Esther', phone_number='0987654321')
        response = self.client.post(self.url, {'number': '0987654321'})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'message': 'user does not have units associated yet'})

    def test_worker_has_units(self):
        response = self.client.post(self.url, {'number': '1234567890'})
        self.assertEqual(response.status_code, 200)
        expected_units = json.dumps(list(Unit.objects.filter(worker=self.worker).values('pk', 'name')))
        self.assertJSONEqual(response.content, {'units': expected_units})


class MakeVisitTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.worker = Worker.objects.create(name='Abdulwali', phone_number='1234567890')
        self.unit = Unit.objects.create(name='Unit 1', worker=self.worker)
        self.url = reverse('make_visit', kwargs={'pk': self.unit.pk, 'longitude': 12.34, 'latitude': 56.78})

    def test_unit_does_not_exist(self):
        url = reverse('make_visit', kwargs={'pk': 9999, 'longitude': 12.34, 'latitude': 56.78})
        response = self.client.post(url, {'number': '1234567890'})
        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(response.content, {'message': 'Unit does not exist'})

    def test_worker_not_associated_with_unit(self):
        new_worker = Worker.objects.create(name='Jane Doe', phone_number='0987654321')
        response = self.client.post(self.url, {'number': '0987654321'})
        self.assertEqual(response.status_code, 403)
        self.assertJSONEqual(response.content, {'message': 'You are not associated with this unit'})

    def test_successful_visit_creation(self):
        response = self.client.post(self.url, {'number': '1234567890'})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'message': 'visit created successfully'})
        self.assertEqual(Visit.objects.count(), 1)
        visit = Visit.objects.first()
        self.assertEqual(visit.unit, self.unit)
        self.assertEqual(visit.longitude, 12.34)
        self.assertEqual(visit.latitude, 56.78)
