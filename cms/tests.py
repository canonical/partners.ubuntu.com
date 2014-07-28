import json

from django.test import TestCase
from django.test.client import Client

from cms.models import Partner

c = Client()

class APITestCase(TestCase):
    def setUp(self):
        Partner.objects.create(
            name="Vendor", 
            slug="vendor",
            published=True,
            featured=True,
            generate_page=False
        )

    def test_get_slug(self):
        response = c.get('/partners.json', {'name': 'Vendor'})
        json_response = json.loads(response.content)
        self.assertEqual(json_response[0]['slug'], 'vendor')

    def test_get_all(self):
        response = c.get('/partners.json')
        json_response = json.loads(response.content)
        self.assertEqual(json_response[0]['slug'], 'vendor')

    def test_get_nothing(self):
        response = c.get('/partners.json', {'name': 'nothing-here'})
        json_response = json.loads(response.content)
        self.assertEqual(len(json_response), 0)

    def test_bad_querystring(self):
        response = c.get('/partners.json', {'nothing': 'nothing-here'})
        self.assertEqual(response.status_code, 200)

    def test_bad_type(self):
        response = c.get('/partners.json', {'programme': 'nothing-here'})
        self.assertEqual(response.status_code, 400)