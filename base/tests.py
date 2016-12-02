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

class StudentTests(TestCase):

    def setUp(self):
        self.client = Client()

    def basic_post_test(self):

        student = self.client.add('/students/',
        {
            name: "Example Student",
            email: "student.e@husky.neu.edu"
            classes: [
                00000,
                00001
            ],
            projects: [
                00000,
                00001
            ],
        })
        self.assertEqual(student.status_code, 201)
        self.assertEqual(student.context['name'], "Example Student")
        self.assertEqual(student.context['email'], "student.e@husky.neu.edu")
        self.assertEqual(len(student.context['classes']), 2)
        self.assertEqual(len(student.context['projects']), 2)

    def test_post_bad_name(self):
        # test null name
        student = self.client.add('/students/',
        {
            name: null,
            email: "student.e@husky.neu.edu"
            classes: [],
            projects: [],
        })
        self.assertEqual(student.status_code, 422)

        # test non-string name
        student = self.client.add('/students/',
        {
            name: 45,
            email: "student.e@husky.neu.edu"
            classes: [],
            projects: [],
        })
        self.assertEqual(student.status_code, 422)

    def test_post_bad_email(self):
        # test null email
        student = self.client.add('/students/',
        {
            name: "Example Student",
            email: null,
            classes: [],
            projects: [],
        })
        self.assertEqual(student.status_code, 422)

        # test non-string email
        student = self.client.add('/students/',
        {
            name: 45,
            email: "student.e@husky.neu.edu"
            classes: [],
            projects: [],
        })
        self.assertEqual(student.status_code, 422)

    def test_post_bad_classes(self):
        # test null classes
        student = self.client.add('/students/',
        {
            name: "Exmaple Student",
            email: "student.e@husky.neu.edu"
            classes: null,
            projects: [],
        })
        self.assertEqual(student.status_code, 422)

        # test non-array classes
        student = self.client.add('/students/',
        {
            name: "Exmaple Student",
            email: "student.e@husky.neu.edu"
            classes: 45,
            projects: [],
        })
        self.assertEqual(student.status_code, 422)

    def test_post_bad_projects(self):
        # test null projects
        student = self.client.add('/students/',
        {
            name: "Exmaple Student",
            email: "student.e@husky.neu.edu"
            classes: [],
            projects: null,
        })
        self.assertEqual(student.status_code, 422)

        # test non-array projects
        student = self.client.add('/students/',
        {
            name: "Exmaple Student",
            email: "student.e@husky.neu.edu"
            classes: [],
            projects: 45,
        })
        self.assertEqual(student.status_code, 422)

    def basic_get_test(self):
        tempStudent = self.client.add('/students/',
        {
            name: "Exmaple Student",
            email: "student.e@husky.neu.edu"
            classes: [],
            projects: [],
        })
        student = self.client.get('/students/', tempStudent.context['id'])
        self.assertEqual(student.context['name'], tempStudent.context['name'])
        self.assertEqual(student.context['email'], tempStudent.context['email'])
        self.assertEqual(len(student.context['classes']), len(tempStudent.context['classes']))
        self.assertEqual(len(student.context['projects'], len(tempStudent.context['projects']))

    def bad_get_test(self):
        student = self.client.get('/students/', "bad")
        self.assertEqual(student.status_code, 422)
        student = self.client.get('/students/', null)
        self.assertEqual(student.status_code, 422)
