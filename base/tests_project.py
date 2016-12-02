from django.test import TestCase
from django.test import Client
from base.models import *
import json

class ProjectTests(TestCase):

    def setUp(self):
        self.client = Client()

    def test_basic_post(self):
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
        p0_json_string = json.loads(project0.content.decode('utf-8'))
        self.assertEqual(project0.status_code, 201)
        self.assertEqual(p0_json_string['name'], "Service Learning Time Tracker")
        self.assertEqual(p0_json_string['course'], "CS4500")
        self.assertEqual(p0_json_string['community_partner'], cp0_json_string['id'])
        self.assertEqual(p0_json_string['description'], "Time Tracking")
        self.assertEqual(p0_json_string['start_date'], "2016-12-12")
        self.assertEqual(p0_json_string['end_date'], "2016-12-13")
        self.assertEqual(p0_json_string['longitude'], "40.000000")
        self.assertEqual(p0_json_string['latitude'], "30.000000")

    def test_bad_post_no_name(self):
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
            "community_partner": cp0_json_string['id'],
            "course": course.id,
            "description": "Time Tracking",
            "start_date": "2016-12-12",
            "end_date": "2016-12-13",
            "longitude": "40.0",
            "latitude": "30.0"
        })
        self.assertEqual(project0.status_code, 400)

    def test_bad_post_no_course(self):
        project0 = self.client.post('/project/',
        {
            "name": "Service Learning Time Tracker",
            "description": "Time Tracking",
            "start_date": "2016-12-12",
            "end_date": "2016-12-13",
            "longitude": "40.0",
            "latitude": "30.0"
        })
        self.assertEqual(project0.status_code, 400)

    def test_bad_post_no_community_partner(self):
        college = College(name='Example College')
        college.save()
        department = Department(name='Example Department', college=college)
        department.save()
        course = Course(id='CS4500', name='Software Development', department=department)
        course.save()

        project0 = self.client.post('/project/',
        {
            "name": "Service Learning Time Tracker",
            "course": course.id,
            "description": "Time Tracking",
            "start_date": "2016-12-12",
            "end_date": "2016-12-13",
            "longitude": "40.0",
            "latitude": "30.0"
        })
        self.assertEqual(project0.status_code, 400)

    def test_bad_post_no_start_date(self):
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
            "end_date": "2016-12-13",
            "longitude": "40.0",
            "latitude": "30.0"
        })
        self.assertEqual(project0.status_code, 400)

    def test_bad_post_no_end_date(self):
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
            "longitude": "40.0",
            "latitude": "30.0"
        })
        self.assertEqual(project0.status_code, 400)

    def test_update(self):
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

        communityPartner1 = self.client.post('/communityPartner/',
        {
          "name": "Example Community Partner 1"
        })
        cp1_json_string = json.loads(communityPartner1.content.decode('utf-8'))
        p0_json_string = json.loads(project0.content.decode('utf-8'))

        temp_dict = {
          "id": p0_json_string['id'],
          "name": "Updated SL Time Tracker",
          "course": course.id,
          "community_partner": cp1_json_string['id'],
          "description": "Updated Time Tracking",
          "start_date": "2017-11-11",
          "end_date": "2017-12-11",
          "longitude": "20.0",
          "latitude": "10.0"
        }

        project0Updated = self.client.put('/project/'+ str(p0_json_string['id']) + '/', json.dumps(temp_dict), content_type="application/json")
        p0u_json_string = json.loads(project0Updated.content.decode('utf-8'))
        self.assertEqual(project0Updated.status_code, 201)
        self.assertEqual(p0u_json_string['name'], "Updated SL Time Tracker")
        self.assertEqual(p0u_json_string['course'], "CS4500")
        self.assertEqual(p0u_json_string['community_partner'], cp1_json_string['id'])
        self.assertEqual(p0u_json_string['description'], "Updated Time Tracking")
        self.assertEqual(p0u_json_string['start_date'], "2017-11-11")
        self.assertEqual(p0u_json_string['end_date'], "2017-12-11")
        self.assertEqual(p0u_json_string['longitude'], "20.000000")
        self.assertEqual(p0u_json_string['latitude'], "10.000000")

    def test_bad_update(self):
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
        p0_json_string = json.loads(project0.content.decode('utf-8'))
        project0Updated = self.client.put('/project/'+ str(p0_json_string['id']) + '/', json.dumps({}), content_type="application/json")
        self.assertEqual(project0Updated.status_code, 400)

    def test_get(self):
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
        p0_json_string = json.loads(project0.content.decode('utf-8'))
        project1 = self.client.get('/project/' + str(p0_json_string['id']) + '/')
        p1_json_string = json.loads(project1.content.decode('utf-8'))
        self.assertEqual(p1_json_string['id'], p0_json_string['id'])
        self.assertEqual(p0_json_string['course'], "CS4500")
        self.assertEqual(p1_json_string['community_partner'], p0_json_string['community_partner'])
        self.assertEqual(p1_json_string['description'], p0_json_string['description'])
        self.assertEqual(p1_json_string['start_date'], p0_json_string['start_date'])
        self.assertEqual(p1_json_string['end_date'], p0_json_string['end_date'])
        self.assertEqual(p1_json_string['longitude'], p0_json_string['longitude'])
        self.assertEqual(p1_json_string['latitude'], p0_json_string['latitude'])

    def test_bad_get(self):
        project0 = self.client.get('/project/99999/')
        self.assertEqual(project0.status_code, 404)
