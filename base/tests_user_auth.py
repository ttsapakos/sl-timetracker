from django.test import TestCase
from django.test import Client
from base.models import User, UserProfile
import json

class UserAuthTests(TestCase):

    def setUp(self):
        self.client = Client()

    def test_basic_student_register(self):
        user0 = self.client.post('/user/registration/',
        {
            "first_name": "Fa",
            "last_name": "Kename",
            "username": "kename.f@husky.neu.edu",
            "password1": "123456abc",
            "password2": "123456abc",
        })
        u0_json_string = json.loads(user0.content.decode('utf-8'))
        self.assertEqual(user0.status_code, 201)
        self.assertTrue('key' in u0_json_string)

        user = User.objects.get(username='kename.f@husky.neu.edu')
        self.assertEqual(user.userprofile.role, UserProfile.STUDENT)
        self.assertEqual(user.first_name, 'Fa')
        self.assertEqual(user.last_name, 'Kename')
        self.assertEqual(user.username, 'kename.f@husky.neu.edu')

    def test_basic_instructor_register1(self):
        user0 = self.client.post('/user/registration/',
        {
            "first_name": "Fa",
            "last_name": "Kename",
            "username": "kename.f@neu.edu",
            "password1": "123456abc",
            "password2": "123456abc",
        })
        u0_json_string = json.loads(user0.content.decode('utf-8'))
        self.assertEqual(user0.status_code, 201)
        self.assertTrue('key' in u0_json_string)

        user = User.objects.get(username='kename.f@neu.edu')
        self.assertEqual(user.userprofile.role, UserProfile.INSTRUCTOR)
        self.assertEqual(user.first_name, 'Fa')
        self.assertEqual(user.last_name, 'Kename')
        self.assertEqual(user.username, 'kename.f@neu.edu')


    def test_basic_instructor_register2(self):
        user0 = self.client.post('/user/registration/',
        {
            "first_name": "Fa",
            "last_name": "Kename",
            "username": "kename.f@northeastern.edu",
            "password1": "123456abc",
            "password2": "123456abc",
        })
        u0_json_string = json.loads(user0.content.decode('utf-8'))
        self.assertEqual(user0.status_code, 201)
        self.assertTrue('key' in u0_json_string)

        user = User.objects.get(username='kename.f@northeastern.edu')
        self.assertEqual(user.userprofile.role, UserProfile.INSTRUCTOR)
        self.assertEqual(user.first_name, 'Fa')
        self.assertEqual(user.last_name, 'Kename')
        self.assertEqual(user.username, 'kename.f@northeastern.edu')

    def test_invalid_domain_register(self):
        user0 = self.client.post('/user/registration/',
        {
            "first_name": "Fa",
            "last_name": "Kename",
            "username": "kename.f@gmail.com",
            "password1": "123456abc",
            "password2": "123456abc",
        })
        u0_json_string = json.loads(user0.content.decode('utf-8'))
        self.assertEqual(user0.status_code, 400)
        self.assertEqual(u0_json_string['username'][0], "Not a valid Northeastern email address.")

    def test_no_username_register(self):
        user0 = self.client.post('/user/registration/',
        {
            "first_name": "Fa",
            "last_name": "Kename",
            "password1": "123456abc",
            "password2": "123456abc",
        })
        u0_json_string = json.loads(user0.content.decode('utf-8'))
        self.assertEqual(user0.status_code, 400)
        self.assertEqual(u0_json_string['username'][0], "This field is required.")

    def test_blank_username_register(self):
        user0 = self.client.post('/user/registration/',
        {
            "first_name": "Fa",
            "last_name": "Kename",
            "username": "",
            "password1": "123456abc",
            "password2": "123456abc",
        })
        u0_json_string = json.loads(user0.content.decode('utf-8'))
        self.assertEqual(user0.status_code, 400)
        self.assertEqual(u0_json_string['username'][0], "This field may not be blank.")

    def test_login_success(self):
        user0 = self.client.post('/user/registration/',
        {
            "first_name": "Fa",
            "last_name": "Kename",
            "username": "kename.f@husky.neu.edu",
            "password1": "123456abc",
            "password2": "123456abc",
        })
        login0 = self.client.post('/user/login/',
        {
            "username": "kename.f@husky.neu.edu",
            "password": "123456abc",
        })
        l0_json_string = json.loads(login0.content.decode('utf-8'))
        self.assertEqual(login0.status_code, 200)

        self.assertTrue('key' in l0_json_string)

    def test_login_fail(self):
        user0 = self.client.post('/user/registration/',
        {
            "first_name": "Fa",
            "last_name": "Kename",
            "username": "kename.f@husky.neu.edu",
            "password1": "123456abc",
            "password2": "123456abc",
        })
        login0 = self.client.post('/user/login/',
        {
            "username": "kename.f@husky.neu.edu",
            "password": "11111111",
        })
        l0_json_string = json.loads(login0.content.decode('utf-8'))
        self.assertEqual(login0.status_code, 400)

        self.assertEqual(l0_json_string['non_field_errors'][0], "Unable to log in with provided credentials.")

    def test_login_blank_pass(self):
        user0 = self.client.post('/user/registration/',
        {
            "first_name": "Fa",
            "last_name": "Kename",
            "username": "kename.f@husky.neu.edu",
            "password1": "123456abc",
            "password2": "123456abc",
        })
        login0 = self.client.post('/user/login/',
        {
            "username": "kename.f@husky.neu.edu",
            "password": "",
        })
        l0_json_string = json.loads(login0.content.decode('utf-8'))
        self.assertEqual(login0.status_code, 400)

        self.assertEqual(l0_json_string['password'][0], "This field may not be blank.")


    def test_logout_success(self):
        user0 = self.client.post('/user/registration/',
        {
            "first_name": "Fa",
            "last_name": "Kename",
            "username": "kename.f@husky.neu.edu",
            "password1": "123456abc",
            "password2": "123456abc",
        })
        login0 = self.client.post('/user/login/',
        {
            "username": "kename.f@husky.neu.edu",
            "password": "123456abc",
        })
        l0_json_string = json.loads(login0.content.decode('utf-8'))
        self.assertEqual(login0.status_code, 200)

        self.assertTrue('key' in l0_json_string)
        key = l0_json_string['key']

        logout0 = self.client.post('/user/logout/',
        {
            "token": key,
        })
        l1_json_string = json.loads(logout0.content.decode('utf-8'))
        self.assertEqual(logout0.status_code, 200)

    def test_user_me(self):
        user1 = self.client.post('/user/registration/',
        {
            "first_name": "Test",
            "last_name": "User",
            "username": "Test@husky.neu.edu",
            "password1": "123456abc",
            "password2": "123456abc",
        })
        u1_json_string = json.loads(user1.content.decode('utf-8'))
        self.assertEqual(user1.status_code, 201)
        self.assertTrue('key' in u1_json_string)
        key = u1_json_string['key']

        user = User.objects.get(username='Test@husky.neu.edu')
        self.assertEqual(user.userprofile.role, UserProfile.STUDENT)
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User')
        self.assertEqual(user.username, 'Test@husky.neu.edu')

        auth_headers = {
            'AUTHORIZATION': 'Token ' + u1_json_string['key'],
        }
        me = self.client.get('/me/', **auth_headers)
        m_json_string = json.loads(me.content.decode('utf-8'))
        self.assertEqual(me.status_code, 200)
        self.assertEqual(m_json_string['first_name'], "Test")
        self.assertEqual(m_json_string['last_name'], "User")
        self.assertEqual(m_json_string['username'], "Test@husky.neu.edu")
        self.assertEqual(m_json_string['role'], UserProfile.STUDENT)
        self.assertEqual(m_json_string['id'], user.id)

    def test_user_me_bad(self):
        me = self.client.get('/me/')
        m_json_string = json.loads(me.content.decode('utf-8'))
        self.assertEqual(me.status_code, 404)
