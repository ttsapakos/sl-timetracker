from django.test import TestCase
from django.test import Client
from base.models import *

class CollegeModelTests(TestCase):
    def test_create_model(self):
        college = College(name="Test College")
        self.assertEqual(college.name, "Test College")
