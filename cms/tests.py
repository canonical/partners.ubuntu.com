import json

from django.test import TestCase
from django.test.client import Client

from cms.models import Partner

c = Client()


class APITestCase(TestCase):
    """
    Tests /partners.json
    """

    def setUp(self):
        Partner.objects.create(
            name="Vendor",
            slug="vendor",
            published=True,
            featured=True,
            dedicated_partner_page=False,
        )

    def test_get_slug(self):
        """
        Grab one partner by querying it by its slug.
        """
        response = c.get("/partners.json", {"name": "Vendor"})
        json_response = json.loads(response.content)
        self.assertEqual(json_response[0]["slug"], "vendor")

    def test_get_all(self):
        """
        Check that the all partners list has our partner as the first item.
        """
        response = c.get("/partners.json")
        json_response = json.loads(response.content)
        self.assertEqual(json_response[0]["slug"], "vendor")

    def test_get_nothing(self):
        """
        A query for a non-existant name should return nothing.
        """
        response = c.get("/partners.json", {"name": "nothing-here"})
        json_response = json.loads(response.content)
        self.assertEqual(len(json_response), 0)

    def test_bad_querystring(self):
        """
        If the user is making up parameters, they should be ignored.
        """
        response = c.get("/partners.json", {"nothing": "nothing-here"})
        json_response = json.loads(response.content)
        self.assertEqual(json_response[0]["slug"], "vendor")
        self.assertEqual(response.status_code, 200)

    def test_unique_partners(self):
        """
        Ensure partners are not duplicated.
        """
        response = c.get("/partners.json")
        json_response = json.loads(response.content)
        self.assertEqual(
            len(json_response), len(set([r["name"] for r in json_response]))
        )
