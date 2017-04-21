from django.test import TestCase
from django.test import Client
from base.models import College
import json

class CollegeTests(TestCase):

    def setUp(self):
        self.client = Client()

    def test_basic_post(self):
        c0 = self.client.post('/college/',
        {
            "name": "College of Testing"
        })
        c0_json_string = json.loads(c0.content.decode('utf-8'))
        self.assertEqual(c0.status_code, 201)
        self.assertEqual(c0_json_string['name'], "College of Testing")

    def test_post_no_name(self):
        c0 = self.client.post('/college/', {})
        self.assertEqual(c0.status_code, 400)

    def test_update(self):
        c0 = self.client.post('/college/',
        {
            "name": "College of Testing"
        })
        c0_json_string = json.loads(c0.content.decode('utf-8'))

        temp_dict = {
            "name": "New Name!"
        }

        c0Updated = self.client.put('/college/' + str(c0_json_string['name']) + '/', json.dumps(temp_dict), content_type="application/json")
        c0Updated_json_string = json.loads(c0Updated.content.decode('utf-8'))
        self.assertEqual(c0Updated_json_string['name'], "New Name!")

    def test_get(self):
        c0 = self.client.post('/college/',
        {
            "name": "College of Test"
        })
        c0_json_string = json.loads(c0.content.decode('utf-8'))
        c1 = self.client.get('/college/' + str(c0_json_string['name']) + '/')
        c1_json_string = json.loads(c1.content.decode('utf-8'))
        self.assertEqual(c1_json_string['name'], c0_json_string['name'])

    def test_bad_get(self):
        c0 = self.client.get('/college/boo/')
        self.assertEqual(c0.status_code, 404)

    def test_delete(self):
        c0 = self.client.post('/college/',
        {
            "name": "College of Testing"
        })
        c0_json_string = json.loads(c0.content.decode('utf-8'))
        deleted = self.client.delete('/college/' + c0_json_string["name"] + '/')
        self.assertEqual(deleted.status_code, 204)

    def test_get_all(self):
        c0 = self.client.post('/college/',
        {
            "name": "College of Test"
        })
        c1 = self.client.post('/college/',
        {
            "name": "College of Tast"
        })
        colleges = self.client.get('/colleges/')
        colleges_json_string = json.loads(colleges.content.decode('utf-8'))
        self.assertEqual(colleges_json_string[0]['name'], "College of Tast")
        self.assertEqual(colleges_json_string[1]['name'], "College of Test")
