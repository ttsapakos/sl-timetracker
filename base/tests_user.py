from django.test import TestCase
from django.test import Client
from base.models import User, UserProfile
import json

class CommunityPartnerTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user1 = User(username="kename.f@neu.edu", first_name="Fa", password="password1")
        self.user1.save()
        self.user2 = User(username="kename.f@husky.neu.edu", first_name="Fa", password="password2")
        self.user2.save()

    def test_get_users(self):
        user_list = self.client.get('/users/')
        u_json_string = json.loads(user_list.content.decode('utf-8'))
        self.assertEqual(user_list.status_code, 200)
        self.assertEqual(u_json_string[0]['username'], "kename.f@neu.edu")
        self.assertEqual(u_json_string[1]['username'], "kename.f@husky.neu.edu")
        self.assertEqual(u_json_string[0]['role'], UserProfile.INSTRUCTOR)
        self.assertEqual(u_json_string[1]['role'], UserProfile.STUDENT)
        self.assertEqual(u_json_string[0]['first_name'], "Fa")
        self.assertEqual(u_json_string[1]['first_name'], "Fa")

    def test_get_user_detail(self):
        user_detail1 = self.client.get('/users/%s/' % self.user1.pk)
        u1_json_string = json.loads(user_detail1.content.decode('utf-8'))
        user_detail2 = self.client.get('/users/%s/' % self.user2.pk)
        u2_json_string = json.loads(user_detail2.content.decode('utf-8'))
        self.assertEqual(user_detail1.status_code, 200)
        self.assertEqual(user_detail2.status_code, 200)
        self.assertEqual(u1_json_string['username'], "kename.f@neu.edu")
        self.assertEqual(u2_json_string['username'], "kename.f@husky.neu.edu")
        self.assertEqual(u1_json_string['role'], UserProfile.INSTRUCTOR)
        self.assertEqual(u2_json_string['role'], UserProfile.STUDENT)
        self.assertEqual(u1_json_string['first_name'], "Fa")
        self.assertEqual(u2_json_string['first_name'], "Fa")

    def test_get_bad_user_detail(self):
        user_detail = self.client.get('/users/9999/')
        u_json_string = json.loads(user_detail.content.decode('utf-8'))
        self.assertEqual(user_detail.status_code, 404)
        self.assertEqual(u_json_string['detail'], "Not found.")

    def test_get_put_user(self):
        self.assertEqual(self.user1.userprofile.role, UserProfile.INSTRUCTOR)
        self.assertEqual(self.user1.first_name, "Fa")
        user_put = self.client.put('/users/%s/' % self.user1.pk,
        {
            "first_name": "Hello",
            "username": "kename.f@neu.edu",
            "role": UserProfile.STUDENT,
        },)
        u_json_string = json.loads(user_put.content.decode('utf-8'))
        print(u_json_string)
        self.assertEqual(user_put.status_code, 200)
        self.assertEqual(self.user1.userprofile.role, UserProfile.STUDENT)
        self.assertEqual(self.user1.first_name, "Hello")
