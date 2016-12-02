from django.test import TestCase
from django.test import Client
from django.test import *
import json

# Create your tests here.

class ExampleMethodTests(TestCase):

    def test_basic_example_addition(self):
        self.assertIs(1+1, 2)
    
    def test_basic_example_strings(self):
        self.assertIs("this is a test", "this is a test")

class DepartmentTests(TestCase):
    
    def setUP(self):
        self.client = Client()
        
    def test_good_post(self):
        department0 = self.client.post('/department/',
        {
            "name": "Trash Department",
            "college": "College of Garbology"
        })
        d0_json_string = json.loads(department0.content.decode('utf-8'))
        self.assertEqual(department0.status_code, 201)
        self.assertEqual(d0_json_string['name'], "Trash Department")
        self.assertEqual(d0_json_string['college'], "College of Garbology")
        
    def test_bad_post_no_name(self):
        department0 = self.client.post('/department/',
        {
            "college": "College of Art"
        })
        self.assertEqual(department0.status_code, 400)
        
    def test_bad_post_null_name(self):
        department0 = self.client.post('/department/',
        {
            "name": None,
            "college": "College of the Void"
        })
        self.assertEqual(department0.status_code, 400)
        
    def test_bad_post_noStr_name(self):
        department0 = self.client.post('/department/',
        {
            "name": 42,
            "college": "College of Everything"
        })
        self.assertEqual(department0.status_code, 400)
        
    
    def test_bad_post_no_college(self):
        department0 = self.client.post('/department/',
        {
            "Name": "Department of Nothingness"
        })
        self.assertEqual(department0.status_code, 400)
        
    def test_bad_post_null_college(self):
        department0 = self.client.post('/department/',
        {
            "name": "The Department",
            "college": None
        })
        self.assertEqual(department0.status_code, 400)
        
    def test_bad_post_noStr_college(self):
        department0 = self.client.post('/department/',
        {
            "name": "Department of One",
            "college": 1234
        })
        self.assertEqual(department0.status_code, 400)
        
    def test_get_good(self):
        department0 = self.client.post('/department/',
        {
            "name": "Department of Defence",
            "college": "College of the Cabinet"
        })
        self.assertEqual(department0.status_code, 201)
        d0_json_string = json.loads(department0.content.decode('utf-8'))
        department1 = self.client.get('/department/' + str(d0_json_string['id']) + '/')
        d1_json_string = json.loads(department1.content.decode('utf-8'))
        self.assertEqual(d1_json_string['id'], d0_json_string['id'])
        self.assertEqual(d1_json_string['name'], d0_json_string['name'])
        self.assertEqual(d1_json_string['college'], d0_json_string['college'])

    def test_bad_get(self):
            department0 = self.client.post('/department/',
            {
                "name": "MissingNo  Department",
                "college": "School of Glitches"
            })
            self.assertEqual(department0.status_code, 201)
            d0_json_string = json.loads(department0.content.decode('utf-8'))
            department1 = self.client.get('/department/' + str(d0_json_string['id'] + 1) + '/')

    def test_good_put(self):
        department0 = self.client.post('/department/',
        {
            "name": "Department of Red Shirts",
            "college": "College of Enterprise"
        })
        d0_json_string = json.loads(department0.content.decode('utf-8'))
        self.assertEqual(department0.status_code, 201)
        
        department1 = self.client.put('/department/' + str(d0_json_string['id']) + '/',
        {
            "name": "Department of Yellow Shirts",
            "college": "College of Australia"
        })
        d1_json_string = json.loads(department1.content.decode('utf-8'))
        self.assertEqual(d1_json_string['id'], d0_json_string['id'])
        self.assertEqual(d1_json_string['name'], "Department of Yellow Shirts")
        self.assertEqual(d1_json_string['college'], "College of Australia")
        
    def test_bad_put(self):
        department0 = self.client.post('/department/',
        {
            "name": "Deep Department",
            "college": "College of Oceanography"
        })
        d0_json_string = json.loads(department0.content.decode('utf-8'))
        self.assertEqual(department0.status_code, 201)
        
        department1 = self.client.put('/department/' + str(d0_json_string['id']) + '/', {})
        d1_json_string = json.loads(department1.content.decode('utf-8'))
        self.assertEqual(department0.status_code, 400)
        

    def test_good_delete(self):
        department0 = self.client.post('/department/',
        {
            "name": "Expendible Department",
            "college": "College of Ephemerality"
        })
        d0_json_string = json.loads(department0.content.decode('utf-8'))
        self.assertEqual(department0.status_code, 201)
        
        department1 = self.client.delete('/department/' + str(d0_json_string['id']) + '/')
        d1_json_string = json.loads(department1.content.decode('utf-8'))
        self.assertEqual(department0.status_code, 204)
        

    def test_bad_delete(self):
        department0 = self.client.post('/department/',
        {
            "name": "Indestructible Department",
            "college": "College of Oceanography"
        })
        d0_json_string = json.loads(department0.content.decode('utf-8'))
        self.assertEqual(department0.status_code, 201)
        
        department1 = self.client.delete('/department/' + str(d0_json_string['id'] + 1) + '/')
        d1_json_string = json.loads(department1.content.decode('utf-8'))
        self.assertEqual(department0.status_code, 400)
        
        
