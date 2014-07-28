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
    	self.response = c.get('/partners.json', {'name': 'Vendor'})
    	self.json_response = json.loads(self.response.content)

    def test_(self):
		self.assertEqual(self.json_response[0]['slug'], 'vendor')
