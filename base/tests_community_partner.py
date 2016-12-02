from django.test import TestCase
from django.test import Client
from base.models import *
import json

class CommunityPartnerTests(TestCase):

    def setUp(self):
        self.client = Client()

    def test_basic_post(self):
        communityPartner0 = self.client.post('/communityPartner/',
        {
            "name": "Example Community Partner 0"
        })
        cp0_json_string = json.loads(communityPartner0.content.decode('utf-8'))
        self.assertEqual(communityPartner0.status_code, 201)
        self.assertEqual(cp0_json_string['name'], "Example Community Partner 0")

    def test_post_no_name(self):
        communityPartner0 = self.client.post('/communityPartner/', {})
        self.assertEqual(communityPartner0.status_code, 400)

    def test_update(self):
        communityPartner0 = self.client.post('/communityPartner/',
        {
            "name": "Example Community Partner 0"
        })
        cp0_json_string = json.loads(communityPartner0.content.decode('utf-8'))

        temp_dict = {
            "id": cp0_json_string['id'],
            "name": "Updated Community Partner Name"
        }

        communityPartner0Updated = self.client.put('/communityPartner/' + str(cp0_json_string['id']) + '/', json.dumps(temp_dict), content_type="application/json")
        cp0Updated_json_string = json.loads(communityPartner0Updated.content.decode('utf-8'))
        self.assertEqual(cp0Updated_json_string['id'], cp0_json_string['id'])
        self.assertEqual(cp0Updated_json_string['name'], "Updated Community Partner Name")

    def test_get(self):
        communityPartner0 = self.client.post('/communityPartner/',
        {
            "name": "Example Community Partner 0"
        })
        cp0_json_string = json.loads(communityPartner0.content.decode('utf-8'))
        communityPartner1 = self.client.get('/communityPartner/' + str(cp0_json_string['id']) + '/')
        cp1_json_string = json.loads(communityPartner1.content.decode('utf-8'))
        self.assertEqual(cp1_json_string['id'], cp0_json_string['id'])
        self.assertEqual(cp1_json_string['name'], cp0_json_string['name'])

    def test_bad_get(self):
        communityPartner0 = self.client.get('/communityPartner/99999/')
        self.assertEqual(communityPartner0.status_code, 404)
