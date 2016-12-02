from django.test import TestCase
from django.test import Client
from base.models import *
import json

# Create your tests here.

class ExampleMethodTests(TestCase):

    def test_basic_example_addition(self):
        self.assertIs(1+1, 2)

    def test_basic_example_strings(self):
        self.assertIs("this is a test", "this is a test")

class ClassTests(TestCase):

    def setUp(self):
        self.client = Client()


    def basic_post_test(self):
        class0 = self.client.add('/classes',
        {
            "id": 00000,
            "name": "Software Development",
            "professors": [
                00000,
                11111,
                22222,
            ],
            "students": [
                00000,
                11111,
                22222,
                33333,
                44444,
                55555,
                66666,
                77777,
                88888,
                99999
            ],
            "projects": [
                00000,
                11111,
                22222,
                33333,
                44444
            ],
            "meeting times": {
                "days": [
                    "M", "W", "R"
                ],
                "time": "9:50:00",
            }
        })
        self.assertEqual(class0.status_code, 201)
        self.assertEqual(class0.context['name'], "Software Development")
        self.assertEqual(len(class0.context['projects']), 5)
        self.assertEqual(len(class0.context['students']), 10)
        self.assertEqual(len(class0.context['professors']), 3)
        self.assertEqual(len(class0.context['meeting times']['days']), 3)

    def bad_post_no_name_test(self):
        class0 = self.client.add('/classes',
        {
            "id": 00000,
            "professors": [
                00000
            ],
            "students": [
                00000
            ],
            "projects": [
                00000
            ],
            "meeting times": {
                "days": [
                    "M", "W", "R"
                ],
                "time": "9:50:00",
            }
        })
        # No name!
        self.assertEqual(class0.status_code, 422)

    def bad_post_no_meeting_time(self):
        class0 = self.client.add('/classes',
        {
            "id": 00000,
            "name": "name",
            "professors": [
                00000
            ],
            "students": [
                00000
            ],
            "projects": [
                00000
            ]
        })
        # No meeting times!
        self.assertEqual(class0.status_code, 422)

    def bad_post_no_professors_test(self):
        class0 = self.client.add('/classes',
        {
            "id": 00000,
            "name": "name",
            "students": [
                00000
            ],
            "projects": [
                00000
            ],
            "meeting times": {
                "days": [
                    "M", "W", "R"
                ],
                "time": "9:50:00",
            }
        })
        # No professors!
        self.assertEqual(class0.status_code, 422)

    def update_test(self):
        class0 = self.client.add('/classes',
        {
            "id": 00000,
            "name": "name",
            "professors": [
                00000
            ],
            "students": [
                00000
            ],
            "projects": [
                00000
            ],
            "meeting times": {
                "days": [
                    "M", "W", "R"
                ],
                "time": "9:50:00",
            }
        })
        self.assertEqual(len(class0.context['professors']), 1)

        class0 = self.client.add('/classes',
        {
            "professors": [
                33333,
                44444,
            ],
            "projects": [
                55555,
                66666,
            ]
        })
        self.assertEqual(len(class0.context['professors']), 2)

    def good_get_test(self):
        temp = self.client.add('/classes',
        {
            "id": 00000,
            "name": "name",
            "professors": [
                00000
            ],
            "students": [
                00000
            ],
            "projects": [
                00000
            ],
            "meeting times": {
                "days": [
                    "M", "W", "R"
                ],
                "time": "9:50:00",
            }
        })

        class0 = self.client.get('/classes/', temp.context['id'])
        self.assertEqual(class0.status_code, 201)
        self.assertEqual(class0.context['name'], "name")
        self.assertEqual(len(class0.context['projects']), 1)
        self.assertEqual(len(class0.context['students']), 1)
        self.assertEqual(len(class0.context['professors']), 1)
        self.assertEqual(len(class0.context['meeting times']['days']), 3)

    def bad_get_test(self):
        class0 = self.client.get('/classes/', 8932)
        self.assertEqual(class0.status_code, 422)

        class0 = self.client.get('/classes/', "8932")
        self.assertEqual(class0.status_code, 422)
