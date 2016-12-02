import unittest
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

class InstructorTests(TestCase):

    def setUp(self):
        self.client = Client()

    def basic_post_test(self):
        instructor = self.client.add('/instructors/',
            {
                name: "Example Instructor",
                role: "professor",
                classes: [
                    "class1",
                    "class2"
                ]
            })
        self.assertEqual(instructor.status_code, 201)
        self.assertEqual(instructor.context['name'], 'Example Instructor')
        self.assertEqual(instructor.context['role'], 'professor')
        self.assertEqual(len(instructor.context['classes']), 2)

    def test_post_bad_name(self):
        # test with null name
        instructor = self.client.add('/instructors/',
            {
                name: null,
                role: "professor",
                classes: []
            })
        self.assertEqual(instructor.status_code, 422)

        # test with non-string name
        instructor = self.client.add('/instructors/',
            {
                name: 45,
                role: "professor",
                classes: []
            })
        self.assertEqual(instructor.status_code, 422)

    def test_post_bad_role(self):
        # test with null role
        instructor = self.client.add('/instructors/',
            {
                name: "Example Professor",
                role: null,
                classes: []
            })
        self.assertEqual(instructor.status_code, 422)

        # test non-string role
        instructor = self.client.add('/instructors/',
            {
                name: "Example Professor",
                role: 45,
                classes: []
            })
        self.assertEqual(instructor.status_code, 422)

    def test_post_bad_classes(self):
        # test with null classes
        instructor = self.client.add('/instructors/',
            {
                name: "Example Professor",
                role: "professor",
                classes: null
            })
        self.assertEqual(instructor.status_code, 422)

        # test with non-array classes
        instructor = self.client.add('/instructors/',
            {
                name: "Example Professor",
                role: "professor",
                classes: 45
            })
        self.assertEqual(instructor.status_code, 422)

    def test_get(self):
        tempInstructor = self.client.add('/instructors/',
            {
                name: "Example Instructor",
                role: "professor",
                classes: []
            })
        instructor = self.client.get('/instructors/', tempInstructor.context['id'])
        assertEqual(instructor.context.status_code, 200)
        assertEqual(tempInstructor.context['name'], instructor.context['name'])
        assertEqual(tempInstructor.context['role'], instructor.context['role'])
        assertEqual(len(tempInstructor.context['classes']), len(instructor.context['classes']))

    def test_bad_get(self):
        instructor = self.client.get('/instructors/', "wrongType")
        assertEqual(instructor.context.status_code, 422)
