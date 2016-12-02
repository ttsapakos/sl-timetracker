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

class CommunityPartnerProjectsTests(TestCase):

    def setUp(self):
        self.client = Client()

    def test_get_projects(self):
        college = College(name='Example College')
        college.save()
        department = Department(name='Example Department', college=college)
        department.save()
        course = Course(id='CS4500', name='Software Development', department=department)
        course.save()

        communityPartner0 = self.client.post('/communityPartner/',
        {
            "name": "Example Community Partner 0"
        })
        cp0_json_string = json.loads(communityPartner0.content.decode('utf-8'))
        project0 = self.client.post('/project/',
        {
            "name": "Service Learning Time Tracker",
            "course": course.id,
            "community_partner": cp0_json_string['id'],
            "description": "Time Tracking",
            "start_date": "2016-12-12",
            "end_date": "2016-12-13",
            "longitude": "40.0",
            "latitude": "30.0"
        })
        project1 = self.client.post('/project/',
        {
            "name": "Credit for Life",
            "course": course.id,
            "community_partner": cp0_json_string['id'],
            "description": "CfL",
            "start_date": "2016-12-16",
            "end_date": "2016-12-20",
            "longitude": "40.0",
            "latitude": "30.0"
        })
        projects1 = self.client.get('/communityPartner/' + str(cp0_json_string['id']) + '/projects/')
        projects1_json_string = json.loads(projects1.content.decode('utf-8'))
        self.assertEqual(projects1.status_code, 200)
        self.assertEqual(len(projects1_json_string), 2)

    def test_get_projects_empty(self):
        communityPartner0 = self.client.post('/communityPartner/',
        {
            "name": "Example Community Partner 0"
        })
        cp0_json_string = json.loads(communityPartner0.content.decode('utf-8'))
        projects1 = self.client.get('/communityPartner/' + str(cp0_json_string['id']) + '/projects/')
        projects1_json_string = json.loads(projects1.content.decode('utf-8'))
        self.assertEqual(projects1.status_code, 200)
        self.assertEqual(len(projects1_json_string), 0)

class CommunityPartnerProjectsActiveTests(TestCase):

    def setUp(self):
        self.client = Client()

    def test_get_projects_active(self):
        college = College(name='Example College')
        college.save()
        department = Department(name='Example Department', college=college)
        department.save()
        course = Course(id='CS4500', name='Software Development', department=department)
        course.save()

        communityPartner0 = self.client.post('/communityPartner/',
        {
            "name": "Example Community Partner 0"
        })
        cp0_json_string = json.loads(communityPartner0.content.decode('utf-8'))
        project0 = self.client.post('/project/',
        {
            "name": "Service Learning Time Tracker",
            "course": course.id,
            "community_partner": cp0_json_string['id'],
            "description": "Time Tracking",
            "start_date": "2016-09-01",
            "end_date": "2016-12-31",
            "longitude": "40.0",
            "latitude": "30.0"
        })
        project1 = self.client.post('/project/',
        {
            "name": "Credit for Life",
            "course": course.id,
            "community_partner": cp0_json_string['id'],
            "description": "CfL",
            "start_date": "2017-09-01",
            "end_date": "2017-12-31",
            "longitude": "40.0",
            "latitude": "30.0"
        })
        projects1 = self.client.get('/communityPartner/' + str(cp0_json_string['id']) + '/projects/active/')
        projects1_json_string = json.loads(projects1.content.decode('utf-8'))
        self.assertEqual(projects1.status_code, 200)
        self.assertEqual(len(projects1_json_string), 1)

    def test_get_projects_active_empty(self):
        communityPartner0 = self.client.post('/communityPartner/',
        {
            "name": "Example Community Partner 0"
        })
        cp0_json_string = json.loads(communityPartner0.content.decode('utf-8'))
        projects1 = self.client.get('/communityPartner/' + str(cp0_json_string['id']) + '/projects/active/')
        projects1_json_string = json.loads(projects1.content.decode('utf-8'))
        self.assertEqual(projects1.status_code, 200)
        self.assertEqual(len(projects1_json_string), 0)
