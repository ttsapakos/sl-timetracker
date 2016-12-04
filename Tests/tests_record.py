import unittest
import sys
import json
from django.test import TestCase
from django.test import Client
from base.models import *
from django.contrib.auth.models import User
from datetime import datetime


# Unit Tests for Record Model

# Note: Django automatically converts type mismatches if it can
# i.e. an integer field that takes in "12" is automatically converted to 12


class ExampleTest(TestCase):
    def test_equal(self):
        self.assertEquals(True, True)
        self.assertEquals("test", "test")

    def test_addition(self):
        self.assertEquals(1 + 1, 2)


# POST TESTS #
class RecordPostTest(TestCase):
    def setUp(self):
        self.Client = Client()

    # creates an example college
    def exampleCollege(self):
        return College(name='Example College')

    # creates an example department
    def exampleDepartment(self):
        college0 = self.exampleCollege()
        college0.save()
        return Department(name='Example Department', college=college0)

    # creates an example course
    def exampleCourse(self):
        department0 = self.exampleDepartment()
        department0.save()
        return Course(id='CS4500', name='Software Development', department=department0)

    # creates an example community_partner
    def exampleCommunityPartner(self):
        return CommunityPartner(name='Example CP0')

    # creates an example project
    def exampleProject(self):
        cp0 = self.exampleCommunityPartner()
        cp0.save()
        course0 = self.exampleCourse()
        course0.save()
        return Project(name="STT", course=course0, community_partner=cp0,
                       description="Time Tracking",start_date="2016-12-12",end_date="2016-12-23",
                       longitude=None,latitude=None)

    # creates an example semester
    def exampleSemester(self):
        return Semester(name='FALL2016', start_date='2016-09-01',end_date='2017-01-01', is_active=True)

    # creates an example category
    def exampleCategory(self):
        return RecordCategory(name='DS')

    # creates an example user
    def exampleUser(self):
        return User(username="ek@ek.ek", email="ek@ek.ek", password="password1")

    # creates an example enrollment
    def exampleEnrollment(self):
        user0 = self.exampleUser()
        user0.save()
        course0 = self.exampleCourse()
        course0.save()
        semester0 = self.exampleSemester()
        semester0.save()
        project0 = self.exampleProject()
        project0.save()
        return Enrollment(user=user0, course=course0, semester=semester0,meeting_days="MWR",
                          meeting_start_time="09:00",meeting_end_time="12:00",project=project0,
                          is_active=1,crn="12345")


    # Simple creation of Record
    # -(id is auto-incremented in database)
    # -optional fields: start_time, Location, comments, extra_field
    def test_basic_post(self):

        enrollment0 = self.exampleEnrollment()
        enrollment0.save()
        project0_id = enrollment0.project.id
        category0 = self.exampleCategory()
        category0.save()
        record = self.client.post('/record/',
                                  {
                                      'enrollment': enrollment0.id,
                                      'project': project0_id,
                                      'date': "2016-11-27",
                                      'start_time': "08:00:00",
                                      'total_hours': 4.50,
                                      'longitude': 42.3399,
                                      'latitude': 71.0891,
                                      'category': category0.name,
                                      'is_active': True,
                                      'comments': "Comments",
                                      'extra_field': "{'employees':[{'firstName':'John', 'lastName':'Doe'}, "
                                                     "{'firstName':'Peter', 'lastName':'Jones'}]}"
                                  })
        record_json_string = json.loads(record.content.decode('utf-8'))
        self.assertEquals(record.status_code, 200)
        self.assertEquals(record_json_string['enrollment'], enrollment0.id)
        self.assertEquals(record_json_string['project'], project0_id)
        self.assertEquals(record_json_string['date'], "2016-11-27")
        self.assertEquals(record_json_string['start_time'], "08:00:00")
        self.assertEquals(record_json_string['total_hours'], '4.50')
        self.assertEquals(record_json_string['longitude'], '42.339900')
        self.assertEquals(record_json_string['latitude'], '71.089100')
        self.assertEquals(record_json_string['category'], "DS")
        self.assertEquals(record_json_string['comments'], "Comments")
        self.assertEquals(record_json_string['extra_field'], "{'employees':[{'firstName':'John', 'lastName':'Doe'}, "
                                                             "{'firstName':'Peter', 'lastName':'Jones'}]}")

    # invalid or missing enrollment
    def test_enrollment(self):
        project0 = self.exampleProject()
        category0 = self.exampleCategory()
        category0.save()
        # null enrollment
        record = self.client.post('/record/',
                                  {
                                      'enrollment': None,
                                      'project': project0.id,
                                      'date': "2016-11-27",
                                      'start_time': "08:00",
                                      'total_hours': 4.5,
                                      'longitude': 42.3399,
                                      'latitude': 71.0891,
                                      'category': category0.name,
                                      'is_active': True,
                                      'comments': "Comments",
                                      'extra_field': "{'employees':[{'firstName':'John', 'lastName':'Doe'}, "
                                                     "{'firstName':'Peter', 'lastName':'Jones'}]}"
                                  })
        self.assertEqual(record.status_code, 400)

        # invalid enrollment (negative int)
        record = self.client.post('/record/',
                                  {
                                      'enrollment': -1,
                                      'project': project0.id,
                                      'date': "2016-11-27",
                                      'start_time': "08:00",
                                      'total_hours': 4.5,
                                      'longitude': 42.3399,
                                      'latitude': 71.0891,
                                      'category': category0.name,
                                      'is_active': True,
                                      'comments': "Comments",
                                      'extra_field': "{'employees':[{'firstName':'John', 'lastName':'Doe'}, "
                                                     "{'firstName':'Peter', 'lastName':'Jones'}]}"
                                  })
        self.assertEqual(record.status_code, 400)

        # invalid enrollment (zero)
        record = self.client.post('/record/',
                                  {
                                      'enrollment': 0,
                                      'project': project0.id,
                                      'date': "2016-11-27",
                                      'start_time': "08:00",
                                      'total_hours': 4.5,
                                      'longitude': 42.3399,
                                      'latitude': 71.0891,
                                      'category': category0.name,
                                      'is_active': True,
                                      'comments': "Comments",
                                      'extra_field': "{'employees':[{'firstName':'John', 'lastName':'Doe'}, "
                                                     "{'firstName':'Peter', 'lastName':'Jones'}]}"
                                  })
        self.assertEqual(record.status_code, 400)

        # invalid enrollment (decimal)
        record = self.client.post('/record/',
                                  {
                                      'enrollment': 12.1,
                                      'project': project0.id,
                                      'date': "2016-11-27",
                                      'start_time': "08:00",
                                      'total_hours': 4.5,
                                      'longitude': 42.3399,
                                      'latitude': 71.0891,
                                      'category': category0.name,
                                      'is_active': True,
                                      'comments': "Comments",
                                      'extra_field': "{'employees':[{'firstName':'John', 'lastName':'Doe'}, "
                                                     "{'firstName':'Peter', 'lastName':'Jones'}]}"
                                  })
        self.assertEqual(record.status_code, 400)

        # invalid enrollment (does not exist)
        record = self.client.post('/record/',
                                  {
                                      'enrollment': 999999,
                                      'project': project0.id,
                                      'date': "2016-11-27",
                                      'start_time': "08:00",
                                      'total_hours': 4.5,
                                      'longitude': 42.3399,
                                      'latitude': 71.0891,
                                      'category': category0.name,
                                      'is_active': True,
                                      'comments': "Comments",
                                      'extra_field': "{'employees':[{'firstName':'John', 'lastName':'Doe'}, "
                                                     "{'firstName':'Peter', 'lastName':'Jones'}]}"
                                  })
        self.assertEqual(record.status_code, 400)

    # invalid or missing project
    def test_project(self):
        enrollment0 = self.exampleEnrollment()
        enrollment0.save()
        category0 = self.exampleCategory()
        category0.save()
        # null project
        record = self.client.post('/record/',
                                  {
                                      'enrollment': enrollment0.id,
                                      'project': None,
                                      'date': "2016-11-27",
                                      'start_time': "08:00:00",
                                      'total_hours': 4.5,
                                      'longitude': 42.3399,
                                      'latitude': 71.0891,
                                      'category': category0.name,
                                      'is_active': True,
                                      'comments': "Comments",
                                      'extra_field': "{'employees':[{'firstName':'John', 'lastName':'Doe'}, "
                                                     "{'firstName':'Peter', 'lastName':'Jones'}]}"
                                  })
        self.assertEqual(record.status_code, 400)

        # invalid project (negative int)
        record = self.client.post('/record/',
                                  {
                                      'enrollment': enrollment0.id,
                                      'project': -1,
                                      'date': "2016-11-27",
                                      'start_time': "08:00:00",
                                      'total_hours': 4.5,
                                      'longitude': 42.3399,
                                      'latitude': 71.0891,
                                      'category': category0.name,
                                      'is_active': True,
                                      'comments': "Comments",
                                      'extra_field': "{'employees':[{'firstName':'John', 'lastName':'Doe'}, "
                                                     "{'firstName':'Peter', 'lastName':'Jones'}]}"
                                  })
        self.assertEqual(record.status_code, 400)

        # invalid project (zero)
        record = self.client.post('/record/',
                                  {
                                      'enrollment': enrollment0.id,
                                      'project': 0,
                                      'date': "2016-11-27",
                                      'start_time': "08:00:00",
                                      'total_hours': 4.5,
                                      'longitude': 42.3399,
                                      'latitude': 71.0891,
                                      'category': category0.name,
                                      'is_active': True,
                                      'comments': "Comments",
                                      'extra_field': "{'employees':[{'firstName':'John', 'lastName':'Doe'}, "
                                                     "{'firstName':'Peter', 'lastName':'Jones'}]}"
                                  })
        self.assertEqual(record.status_code, 400)

        # invalid project (decimal)
        record = self.client.post('/record/',
                                  {
                                      'enrollment': enrollment0.id,
                                      'project': 12.4,
                                      'date': "2016-11-27",
                                      'start_time': "08:00:00",
                                      'total_hours': 4.5,
                                      'longitude': 42.3399,
                                      'latitude': 71.0891,
                                      'category': category0.name,
                                      'is_active': True,
                                      'comments': "Comments",
                                      'extra_field': "{'employees':[{'firstName':'John', 'lastName':'Doe'}, "
                                                     "{'firstName':'Peter', 'lastName':'Jones'}]}"
                                  })
        self.assertEqual(record.status_code, 400)

        # invalid project (does not exist)
        record = self.client.post('/record/',
                                  {
                                      'enrollment': 1,
                                      'project': 99999,
                                      'date': "2016-11-27",
                                      'start_time': "08:00",
                                      'total_hours': 4,
                                      'longitude': 42.3399,
                                      'latitude': 71.0891,
                                      'category': "TO",
                                      'is_active': True,
                                      'comments': "Comments",
                                      'extra_field': None
                                  })
        self.assertEqual(record.status_code, 400)

    # invalid or missing date
    def test_date(self):
        enrollment0 = self.exampleEnrollment()
        enrollment0.save()
        project0_id = enrollment0.project.id
        category0 = self.exampleCategory()
        category0.save()
        # null date
        record = self.client.post('/record/',
                                  {
                                      'enrollment': enrollment0.id,
                                      'project': project0_id,
                                      'date': None,
                                      'start_time': "08:00:00",
                                      'total_hours': 4.5,
                                      'longitude': 42.3399,
                                      'latitude': 71.0891,
                                      'category': category0.name,
                                      'is_active': True,
                                      'comments': "Comments",
                                      'extra_field': "{'employees':[{'firstName':'John', 'lastName':'Doe'}, "
                                                     "{'firstName':'Peter', 'lastName':'Jones'}]}"
                                  })
        self.assertEqual(record.status_code, 400)

        # invalid date (incomplete entry)
        record = self.client.post('/record/',
                                  {
                                      'enrollment': enrollment0.id,
                                      'project': project0_id,
                                      'date': "12-29",
                                      'start_time': "08:00:00",
                                      'total_hours': 4.5,
                                      'longitude': 42.3399,
                                      'latitude': 71.0891,
                                      'category': category0.name,
                                      'is_active': True,
                                      'comments': "Comments",
                                      'extra_field': "{'employees':[{'firstName':'John', 'lastName':'Doe'}, "
                                                     "{'firstName':'Peter', 'lastName':'Jones'}]}"
                                  })
        self.assertEqual(record.status_code, 400)

        # invalid date (non-date string)
        record = self.client.post('/record/',
                                  {
                                      'enrollment': enrollment0.id,
                                      'project': project0_id,
                                      'date': "Hello",
                                      'start_time': "08:00:00",
                                      'total_hours': 4.5,
                                      'longitude': 42.3399,
                                      'latitude': 71.0891,
                                      'category': category0.name,
                                      'is_active': True,
                                      'comments': "Comments",
                                      'extra_field': "{'employees':[{'firstName':'John', 'lastName':'Doe'}, "
                                                     "{'firstName':'Peter', 'lastName':'Jones'}]}"
                                  })
        self.assertEqual(record.status_code, 400)

        # invalid date (decimal)
        record = self.client.post('/record/',
                                  {
                                      'enrollment': enrollment0.id,
                                      'project': project0_id,
                                      'date': 12.01,
                                      'start_time': "08:00:00",
                                      'total_hours': 4.5,
                                      'longitude': 42.3399,
                                      'latitude': 71.0891,
                                      'category': category0.name,
                                      'is_active': True,
                                      'comments': "Comments",
                                      'extra_field': "{'employees':[{'firstName':'John', 'lastName':'Doe'}, "
                                                     "{'firstName':'Peter', 'lastName':'Jones'}]}"
                                  })
        self.assertEqual(record.status_code, 400)

    # invalid start_time
    def test_start_time(self):
        enrollment0 = self.exampleEnrollment()
        enrollment0.save()
        project0_id = enrollment0.project.id
        category0 = self.exampleCategory()
        category0.save()
        # null start_time (VALID)
        record = self.client.post('/record/',
                                  {
                                      'enrollment': enrollment0.id,
                                      'project': project0_id,
                                      'date': "2016-11-27",
                                      'start_time': datetime.now().time(),
                                      'total_hours': 4.50,
                                      'longitude': 42.3399,
                                      'latitude': 71.0891,
                                      'category': category0.name,
                                      'is_active': True,
                                      'comments': "Comments",
                                      'extra_field': "{'employees':[{'firstName':'John', 'lastName':'Doe'}, "
                                                     "{'firstName':'Peter', 'lastName':'Jones'}]}"
                                  })
        self.assertEqual(record.status_code, 200)

        # invalid start_time (int)
        record = self.client.post('/record/',
                                  {
                                      'enrollment': enrollment0.id,
                                      'project': project0_id,
                                      'date': "2016-11-27",
                                      'start_time': 8,
                                      'total_hours': 4.5,
                                      'longitude': 42.3399,
                                      'latitude': 71.0891,
                                      'category': category0.name,
                                      'is_active': True,
                                      'comments': "Comments",
                                      'extra_field': "{'employees':[{'firstName':'John', 'lastName':'Doe'}, "
                                                     "{'firstName':'Peter', 'lastName':'Jones'}]}"
                                  })
        self.assertEqual(record.status_code, 400)

        # invalid start_time (time doesn't exist)
        record = self.client.post('/record/',
                                  {
                                      'enrollment': enrollment0.id,
                                      'project': project0_id,
                                      'date': "2016-11-27",
                                      'start_time': "24:00:01",
                                      'total_hours': 4.5,
                                      'longitude': 42.3399,
                                      'latitude': 71.0891,
                                      'category': category0.name,
                                      'is_active': True,
                                      'comments': "Comments",
                                      'extra_field': "{'employees':[{'firstName':'John', 'lastName':'Doe'}, "
                                                     "{'firstName':'Peter', 'lastName':'Jones'}]}"
                                  })
        self.assertEqual(record.status_code, 400)

        # invalid start_time (non-time string)
        record = self.client.post('/record/',
                                  {
                                      'enrollment': enrollment0.id,
                                      'project': project0_id,
                                      'date': "2016-11-27",
                                      'start_time': "Hello",
                                      'total_hours': 4.5,
                                      'longitude': 42.3399,
                                      'latitude': 71.0891,
                                      'category': category0.name,
                                      'is_active': True,
                                      'comments': "Comments",
                                      'extra_field': "{'employees':[{'firstName':'John', 'lastName':'Doe'}, "
                                                     "{'firstName':'Peter', 'lastName':'Jones'}]}"
                                  })
        self.assertEqual(record.status_code, 400)

    # invalid or missing total_hours
    def test_total_hours(self):
        enrollment0 = self.exampleEnrollment()
        enrollment0.save()
        project0_id = enrollment0.project.id
        category0 = self.exampleCategory()
        category0.save()
        # null total_hours
        record = self.client.post('/record/',
                                  {
                                      'enrollment': enrollment0.id,
                                      'project': project0_id,
                                      'date': "2016-11-27",
                                      'start_time': "08:00:00",
                                      'total_hours': None,
                                      'longitude': 42.3399,
                                      'latitude': 71.0891,
                                      'category': category0.name,
                                      'is_active': True,
                                      'comments': "Comments",
                                      'extra_field': "{'employees':[{'firstName':'John', 'lastName':'Doe'}, "
                                                     "{'firstName':'Peter', 'lastName':'Jones'}]}"
                                  })
        self.assertEqual(record.status_code, 400)

        # invalid total_hours (negative number)
        record = self.client.post('/record/',
                                  {
                                      'enrollment': enrollment0.id,
                                      'project': project0_id,
                                      'date': "2016-11-27",
                                      'start_time': "08:00:00",
                                      'total_hours': -2.2,
                                      'longitude': 42.3399,
                                      'latitude': 71.0891,
                                      'category': category0.name,
                                      'is_active': True,
                                      'comments': "Comments",
                                      'extra_field': "{'employees':[{'firstName':'John', 'lastName':'Doe'}, "
                                                     "{'firstName':'Peter', 'lastName':'Jones'}]}"
                                  })
        self.assertEqual(record.status_code, 400)

        # invalid total_hours (must be greater than zero)
        record = self.client.post('/record/',
                                  {
                                      'enrollment': enrollment0.id,
                                      'project': project0_id,
                                      'date': "2016-11-27",
                                      'start_time': "08:00:00",
                                      'total_hours': 0,
                                      'longitude': 42.3399,
                                      'latitude': 71.0891,
                                      'category': category0.name,
                                      'is_active': True,
                                      'comments': "Comments",
                                      'extra_field': "{'employees':[{'firstName':'John', 'lastName':'Doe'}, "
                                                     "{'firstName':'Peter', 'lastName':'Jones'}]}"
                                  })
        self.assertEqual(record.status_code, 400)

        # valid total_hours (24 hours)
        record = self.client.post('/record/',
                                  {
                                      'enrollment': enrollment0.id,
                                      'project': project0_id,
                                      'date': "2016-11-27",
                                      'start_time': "08:00:00",
                                      'total_hours': 24,
                                      'longitude': 42.3399,
                                      'latitude': 71.0891,
                                      'category': category0.name,
                                      'is_active': True,
                                      'comments': "Comments",
                                      'extra_field': "{'employees':[{'firstName':'John', 'lastName':'Doe'}, "
                                                     "{'firstName':'Peter', 'lastName':'Jones'}]}"
                                  })
        self.assertEqual(record.status_code, 200)

        # invalid total_hours (24.01 hours)
        record = self.client.post('/record/',
                                  {
                                      'enrollment': enrollment0.id,
                                      'project': project0_id,
                                      'date': "2016-11-27",
                                      'start_time': "08:00:00",
                                      'total_hours': 24.01,
                                      'longitude': 42.3399,
                                      'latitude': 71.0891,
                                      'category': category0.name,
                                      'is_active': True,
                                      'comments': "Comments",
                                      'extra_field': "{'employees':[{'firstName':'John', 'lastName':'Doe'}, "
                                                     "{'firstName':'Peter', 'lastName':'Jones'}]}"
                                  })
        self.assertEqual(record.status_code, 400)

    # invalid longitude
    def test_longitude(self):
        enrollment0 = self.exampleEnrollment()
        enrollment0.save()
        project0_id = enrollment0.project.id
        category0 = self.exampleCategory()
        category0.save()
        # null longitude (and latitude) --> VALID
        record = self.client.post('/record/',
                                  {
                                      'enrollment': enrollment0.id,
                                      'project': project0_id,
                                      'date': "2016-11-27",
                                      'start_time': "08:00:00",
                                      'total_hours': 4.5,
                                      'category': category0.name,
                                      'is_active': True,
                                      'comments': "Comments",
                                      'extra_field': "{'employees':[{'firstName':'John', 'lastName':'Doe'}, "
                                                     "{'firstName':'Peter', 'lastName':'Jones'}]}"
                                  })
        self.assertEqual(record.status_code, 200)

        # null longitude (latitude correct) --> INVALID
        record = self.client.post('/record/',
                                  {
                                      'enrollment': enrollment0.id,
                                      'project': project0_id,
                                      'date': "2016-11-27",
                                      'start_time': "08:00:00",
                                      'total_hours': 4.5,
                                      'longitude': None,
                                      'latitude': 71.0123,
                                      'category': category0.name,
                                      'is_active': True,
                                      'comments': "Comments",
                                      'extra_field': "{'employees':[{'firstName':'John', 'lastName':'Doe'}, "
                                                     "{'firstName':'Peter', 'lastName':'Jones'}]}"
                                  })
        self.assertEqual(record.status_code, 400)

        # invalid longitude (non-Decimal)
        record = self.client.post('/record/',
                                  {
                                      'enrollment': enrollment0.id,
                                      'project': project0_id,
                                      'date': "2016-11-27",
                                      'start_time': "08:00:00",
                                      'total_hours': 4.5,
                                      'longitude': "not a number haha!",
                                      'latitude': 71.1012,
                                      'category': category0.name,
                                      'is_active': True,
                                      'comments': "Comments",
                                      'extra_field': "{'employees':[{'firstName':'John', 'lastName':'Doe'}, "
                                                     "{'firstName':'Peter', 'lastName':'Jones'}]}"
                                  })
        self.assertEqual(record.status_code, 400)

        # invalid longitude (max-int)
        record = self.client.post('/record/',
                                  {
                                      'enrollment': enrollment0.id,
                                      'project': project0_id,
                                      'date': "2016-11-27",
                                      'start_time': "08:00:00",
                                      'total_hours': 4.5,
                                      'longitude': sys.maxsize,
                                      'latitude': 81.122,
                                      'category': category0.name,
                                      'is_active': True,
                                      'comments': "Comments",
                                      'extra_field': "{'employees':[{'firstName':'John', 'lastName':'Doe'}, "
                                                     "{'firstName':'Peter', 'lastName':'Jones'}]}"
                                  })
        self.assertEqual(record.status_code, 400)

    # invalid latitude
    def test_latitude(self):
        enrollment0 = self.exampleEnrollment()
        enrollment0.save()
        project0_id = enrollment0.project.id
        category0 = self.exampleCategory()
        category0.save()
        # null latitude (and longitude) --> VALID
        record = self.client.post('/record/',
                                  {
                                      'enrollment': enrollment0.id,
                                      'project': project0_id,
                                      'date': "2016-11-27",
                                      'start_time': "08:00:00",
                                      'total_hours': 4.5,
                                      'category': category0.name,
                                      'is_active': True,
                                      'comments': "Comments",
                                      'extra_field': "{'employees':[{'firstName':'John', 'lastName':'Doe'}, "
                                                     "{'firstName':'Peter', 'lastName':'Jones'}]}"
                                  })
        self.assertEqual(record.status_code, 200)

        # null latitude (longitude correct) --> INVALID
        record = self.client.post('/record/',
                                  {
                                      'enrollment': enrollment0.id,
                                      'project': project0_id,
                                      'date': "2016-11-27",
                                      'start_time': "08:00:00",
                                      'total_hours': 4.5,
                                      'longitude': 72.112,
                                      'category': category0.name,
                                      'is_active': True,
                                      'comments': "Comments",
                                      'extra_field': "{'employees':[{'firstName':'John', 'lastName':'Doe'}, "
                                                     "{'firstName':'Peter', 'lastName':'Jones'}]}"
                                  })
        self.assertEqual(record.status_code, 400)

        # valid latitude (string Decimal)
        record = self.client.post('/record/',
                                  {
                                      'enrollment': enrollment0.id,
                                      'project': project0_id,
                                      'date': "2016-11-27",
                                      'start_time': "08:00:00",
                                      'total_hours': 4.5,
                                      'longitude': 71.213,
                                      'latitude': "12.212",
                                      'category': category0.name,
                                      'is_active': True,
                                      'comments': "Comments",
                                      'extra_field': "{'employees':[{'firstName':'John', 'lastName':'Doe'}, "
                                                     "{'firstName':'Peter', 'lastName':'Jones'}]}"
                                  })
        self.assertEqual(record.status_code, 200)

        # invalid latitude (max-int)
        record = self.client.post('/record/',
                                  {
                                      'enrollment': enrollment0.id,
                                      'project': project0_id,
                                      'date': "2016-11-27",
                                      'start_time': "08:00:00",
                                      'total_hours': 4.5,
                                      'longitude': 71.124,
                                      'latitude': sys.maxsize,
                                      'category': category0.name,
                                      'is_active': True,
                                      'comments': "Comments",
                                      'extra_field': "{'employees':[{'firstName':'John', 'lastName':'Doe'}, "
                                                     "{'firstName':'Peter', 'lastName':'Jones'}]}"
                                  })
        self.assertEqual(record.status_code, 400)

    # invalid or missing category
    def test_category(self):
        enrollment0 = self.exampleEnrollment()
        enrollment0.save()
        project0_id = enrollment0.project.id
        # null category
        record = self.client.post('/record/',
                                  {
                                      'enrollment': enrollment0.id,
                                      'project': project0_id,
                                      'date': "2016-11-27",
                                      'start_time': "08:00:00",
                                      'total_hours': 4.5,
                                      'longitude': 71.124,
                                      'latitude': 72.1217,
                                      'category': None,
                                      'is_active': True,
                                      'comments': "Comments",
                                      'extra_field': "{'employees':[{'firstName':'John', 'lastName':'Doe'}, "
                                                     "{'firstName':'Peter', 'lastName':'Jones'}]}"
                                  })
        self.assertEqual(record.status_code, 400)

        # invalid category (not listed in categories)
        record = self.client.post('/record/',
                                  {
                                      'enrollment': enrollment0.id,
                                      'project': project0_id,
                                      'date': "2016-11-27",
                                      'start_time': "08:00:00",
                                      'total_hours': 4.5,
                                      'longitude': 71.124,
                                      'latitude': 72.1217,
                                      'category': "TD",
                                      'is_active': True,
                                      'comments': "Comments",
                                      'extra_field': "{'employees':[{'firstName':'John', 'lastName':'Doe'}, "
                                                     "{'firstName':'Peter', 'lastName':'Jones'}]}"
                                  })
        self.assertEqual(record.status_code, 400)

        # invalid category (multiple categories listed)
        record = self.client.post('/record/',
                                  {
                                      'enrollment': enrollment0.id,
                                      'project': project0_id,
                                      'date': "2016-11-27",
                                      'start_time': "08:00:00",
                                      'total_hours': 4.5,
                                      'longitude': 71.124,
                                      'latitude': 72.1217,
                                      'category': "TO,DS",
                                      'is_active': True,
                                      'comments': "Comments",
                                      'extra_field': "{'employees':[{'firstName':'John', 'lastName':'Doe'}, "
                                                     "{'firstName':'Peter', 'lastName':'Jones'}]}"
                                  })
        self.assertEqual(record.status_code, 400)

        # invalid category (non-string)
        record = self.client.post('/record/',
                                  {
                                      'enrollment': enrollment0.id,
                                      'project': project0_id,
                                      'date': "2016-11-27",
                                      'start_time': "08:00:00",
                                      'total_hours': 4.5,
                                      'longitude': 71.124,
                                      'latitude': 72.1217,
                                      'category': 121,
                                      'is_active': True,
                                      'comments': "Comments",
                                      'extra_field': "{'employees':[{'firstName':'John', 'lastName':'Doe'}, "
                                                     "{'firstName':'Peter', 'lastName':'Jones'}]}"
                                  })
        self.assertEqual(record.status_code, 400)

    # invalid or missing active indicator
    def test_is_active(self):
        enrollment0 = self.exampleEnrollment()
        enrollment0.save()
        project0_id = enrollment0.project.id
        category0 = self.exampleCategory()
        category0.save()

        # on creation of new model, should default to True
        # null is_active
        record = self.client.post('/record/',
                                  {
                                      'enrollment': enrollment0.id,
                                      'project': project0_id,
                                      'date': "2016-11-27",
                                      'start_time': "08:00:00",
                                      'total_hours': 4.5,
                                      'longitude': 71.124,
                                      'latitude': 72.1217,
                                      'category': category0.name,
                                      'is_active': None,
                                      'comments': "Comments",
                                      'extra_field': "{'employees':[{'firstName':'John', 'lastName':'Doe'}, "
                                                     "{'firstName':'Peter', 'lastName':'Jones'}]}"
                                  })
        self.assertEqual(record.status_code, 400)

        # invalid is_active (non-boolean)
        record = self.client.post('/record/',
                                  {
                                      'enrollment': enrollment0.id,
                                      'project': project0_id,
                                      'date': "2016-11-27",
                                      'start_time': "08:00:00",
                                      'total_hours': 4.5,
                                      'longitude': 71.124,
                                      'latitude': 72.1217,
                                      'category': category0.name,
                                      'is_active': 12,
                                      'comments': "Comments",
                                      'extra_field': "{'employees':[{'firstName':'John', 'lastName':'Doe'}, "
                                                     "{'firstName':'Peter', 'lastName':'Jones'}]}"
                                  })
        self.assertEqual(record.status_code, 400)

        # valid is_active (1)
        record = self.client.post('/record/',
                                  {
                                      'enrollment': enrollment0.id,
                                      'project': project0_id,
                                      'date': "2016-11-27",
                                      'start_time': "08:00:00",
                                      'total_hours': 4.5,
                                      'longitude': 71.124,
                                      'latitude': 72.1217,
                                      'category': category0.name,
                                      'is_active': 1,
                                      'comments': "Comments",
                                      'extra_field': "{'employees':[{'firstName':'John', 'lastName':'Doe'}, "
                                                     "{'firstName':'Peter', 'lastName':'Jones'}]}"
                                  })
        self.assertEqual(record.status_code, 200)

        # valid is_active (False - 0)
        record = self.client.post('/record/',
                                  {
                                      'enrollment': enrollment0.id,
                                      'project': project0_id,
                                      'date': "2016-11-27",
                                      'start_time': "08:00:00",
                                      'total_hours': 4.5,
                                      'longitude': 71.124,
                                      'latitude': 72.1217,
                                      'category': category0.name,
                                      'is_active': 0,
                                      'comments': "Comments",
                                      'extra_field': "{'employees':[{'firstName':'John', 'lastName':'Doe'}, "
                                                     "{'firstName':'Peter', 'lastName':'Jones'}]}"
                                  })
        self.assertEqual(record.status_code, 200)

    # invalid comments
    def test_comments(self):
        enrollment0 = self.exampleEnrollment()
        enrollment0.save()
        project0_id = enrollment0.project.id
        category0 = self.exampleCategory()
        category0.save()
        # null comments --> VALID
        record = self.client.post('/record/',
                                  {
                                      'enrollment': enrollment0.id,
                                      'project': project0_id,
                                      'date': "2016-11-27",
                                      'start_time': "08:00:00",
                                      'total_hours': 4.5,
                                      'longitude': 71.124,
                                      'latitude': 72.1217,
                                      'category': category0.name,
                                      'is_active': True,
                                      'comments': None,
                                      'extra_field': "{'employees':[{'firstName':'John', 'lastName':'Doe'}, "
                                                     "{'firstName':'Peter', 'lastName':'Jones'}]}"
                                  })
        self.assertEqual(record.status_code, 200)

        # valid comments (empty string)
        record = self.client.post('/record/',
                                  {
                                      'enrollment': enrollment0.id,
                                      'project': project0_id,
                                      'date': "2016-11-27",
                                      'start_time': "08:00:00",
                                      'total_hours': 4.5,
                                      'longitude': 71.124,
                                      'latitude': 72.1217,
                                      'category': category0.name,
                                      'is_active': True,
                                      'comments': "",
                                      'extra_field': "{'employees':[{'firstName':'John', 'lastName':'Doe'}, "
                                                     "{'firstName':'Peter', 'lastName':'Jones'}]}"
                                  })
        self.assertEqual(record.status_code, 200)

        # valid comments (decimal casted to string)
        record = self.client.post('/record/',
                                  {
                                      'enrollment': enrollment0.id,
                                      'project': project0_id,
                                      'date': "2016-11-27",
                                      'start_time': "08:00:00",
                                      'total_hours': 4.5,
                                      'longitude': 71.124,
                                      'latitude': 72.1217,
                                      'category': category0.name,
                                      'is_active': True,
                                      'comments': 5.3,
                                      'extra_field': "{'employees':[{'firstName':'John', 'lastName':'Doe'}, "
                                                     "{'firstName':'Peter', 'lastName':'Jones'}]}"
                                  })
        self.assertEqual(record.status_code, 200)

        # valid comments (long-string)
        record = self.client.post('/record/',
                                  {
                                      'enrollment': enrollment0.id,
                                      'project': project0_id,
                                      'date': "2016-11-27",
                                      'start_time': "08:00:00",
                                      'total_hours': 4.5,
                                      'longitude': 71.124,
                                      'latitude': 72.1217,
                                      'category': category0.name,
                                      'is_active': True,
                                      'comments': "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
                                                  "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
                                                  "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
                                                  "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
                                                  "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
                                                  "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
                                                  "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
                                                  "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
                                                  "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
                                                  "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
                                                  "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
                                                  "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
                                                  "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                                      'extra_field': "{'employees':[{'firstName':'John', 'lastName':'Doe'}, "
                                                     "{'firstName':'Peter', 'lastName':'Jones'}]}"
                                  })
        self.assertEqual(record.status_code, 200)

    # invalid extra_field
    def test_extra_field(self):
        enrollment0 = self.exampleEnrollment()
        enrollment0.save()
        project0_id = enrollment0.project.id
        category0 = self.exampleCategory()
        category0.save()
        # null extra_field --> VALID
        record = self.client.post('/record/',
                                  {
                                      'enrollment': enrollment0.id,
                                      'project': project0_id,
                                      'date': "2016-11-27",
                                      'start_time': "08:00:00",
                                      'total_hours': 4.5,
                                      'longitude': 71.124,
                                      'latitude': 72.1217,
                                      'category': category0.name,
                                      'is_active': True,
                                      'comments': "Comments",
                                      'extra_field': None
                                  })
        self.assertEqual(record.status_code, 200)

        # WE HAVE NO VALIDATION ON THE extra_field
        # # invalid extra_field (json of invalid format)
        # record = self.client.post('/record/',
        #                           {
        #                               'enrollment': enrollment0.id,
        #                               'project': project0_id,
        #                               'date': "2016-11-27",
        #                               'start_time': "08:00:00",
        #                               'total_hours': 4.5,
        #                               'longitude': 71.124,
        #                               'latitude': 72.1217,
        #                               'category': category0.name,
        #                               'is_active': True,
        #                               'comments': "Comments",
        #                               'extra_field': "{'employees':[{'firstName':'John', 'lastName':'Doe'}, "
        #                                              "{'firstName':'Peter'}]}"
        #                           })
        # self.assertEqual(record.status_code, 400)


# GET TESTS #
class RecordGetTests(TestCase):
    # creates an example college
    def exampleCollege(self):
        return College(name='Example College')

    # creates an example department
    def exampleDepartment(self):
        college0 = self.exampleCollege()
        college0.save()
        return Department(name='Example Department', college=college0)

    # creates an example course
    def exampleCourse(self):
        department0 = self.exampleDepartment()
        department0.save()
        return Course(id='CS4500', name='Software Development', department=department0)

    # creates an example community_partner
    def exampleCommunityPartner(self):
        return CommunityPartner(name='Example CP0')

    # creates an example project
    def exampleProject(self):
        cp0 = self.exampleCommunityPartner()
        cp0.save()
        course0 = self.exampleCourse()
        course0.save()
        return Project(name="STT", course=course0, community_partner=cp0,
                       description="Time Tracking",start_date="2016-12-12",end_date="2016-12-23",
                       longitude=None,latitude=None)

    # creates an example semester
    def exampleSemester(self):
        return Semester(name='FALL2016', start_date='2016-09-01',end_date='2017-01-01', is_active=True)

    # creates an example category
    def exampleCategory(self):
        return RecordCategory(name='DS')

    # creates an example user
    def exampleUser(self):
        return User(username="ek@ek.ek", email="ek@ek.ek", password="password1")

    # creates an example enrollment
    def exampleEnrollment(self):
        user0 = self.exampleUser()
        user0.save()
        course0 = self.exampleCourse()
        course0.save()
        semester0 = self.exampleSemester()
        semester0.save()
        project0 = self.exampleProject()
        project0.save()
        return Enrollment(user=user0, course=course0, semester=semester0,meeting_days="MWR",
                          meeting_start_time="09:00",meeting_end_time="12:00",project=project0,
                          is_active=1,crn="12345")

    # simple get request for Record
    def test_basic_get(self):
        enrollment0 = self.exampleEnrollment()
        enrollment0.save()
        project0_id = enrollment0.project.id
        category0 = self.exampleCategory()
        category0.save()
        # create a basic record
        record = self.client.post('/record/',
                                  {
                                      'enrollment': enrollment0.id,
                                      'project': project0_id,
                                      'date': "2016-11-27",
                                      'start_time': "08:00:00",
                                      'total_hours': 4.5,
                                      'longitude': 42.3399,
                                      'latitude': 71.0891,
                                      'category': category0.name,
                                      'is_active': True,
                                      'comments': "Comments",
                                      'extra_field': None
                                  })
        record_json_string = json.loads(record.content.decode('utf-8'))
        record2 = self.client.get('/record/' + str(record_json_string['id']) + '/')
        record2_json_string = json.loads(record2.content.decode('utf-8'))
        self.assertEqual(record_json_string['enrollment'], record2_json_string['enrollment'])
        self.assertEqual(record_json_string['date'], record2_json_string['date'])
        self.assertEqual(record_json_string['start_time'], record2_json_string['start_time'])
        self.assertEqual(record_json_string['total_hours'], record2_json_string['total_hours'])
        self.assertEqual(record_json_string['category'], record2_json_string['category'])
        self.assertEqual(record_json_string['is_active'], record2_json_string['is_active'])
        self.assertEqual(record_json_string['comments'], record2_json_string['comments'])
        self.assertEqual(record_json_string['extra_field'], record2_json_string['extra_field'])

    # invalid get request --> id does not exist
    def test_no_id(self):
        record = self.client.get('/record/99999/')
        self.assertEqual(record.status_code, 404)

# PUT TESTS ##
class RecordPutTests(TestCase):
    # creates an example college
    def exampleCollege(self):
        return College(name='Example College')

    # creates an example department
    def exampleDepartment(self):
        college0 = self.exampleCollege()
        college0.save()
        return Department(name='Example Department', college=college0)

    # creates an example course
    def exampleCourse(self):
        department0 = self.exampleDepartment()
        department0.save()
        return Course(id='CS4500', name='Software Development', department=department0)

    # creates an example community_partner
    def exampleCommunityPartner(self):
        return CommunityPartner(name='Example CP0')

    # creates an example project
    def exampleProject(self):
        cp0 = self.exampleCommunityPartner()
        cp0.save()
        course0 = self.exampleCourse()
        course0.save()
        return Project(name="STT", course=course0, community_partner=cp0,
                       description="Time Tracking", start_date="2016-12-12", end_date="2016-12-23",
                       longitude=None, latitude=None)

    # creates an example semester
    def exampleSemester(self):
        return Semester(name='FALL2016', start_date='2016-09-01', end_date='2017-01-01', is_active=True)

    # creates an example category
    def exampleCategory(self):
        return RecordCategory(name='DS')

    # creates an example user
    def exampleUser(self):
        return User(username="ek@ek.ek", email="ek@ek.ek", password="password1")

    # creates an example enrollment
    def exampleEnrollment(self):
        user0 = self.exampleUser()
        user0.save()
        course0 = self.exampleCourse()
        course0.save()
        semester0 = self.exampleSemester()
        semester0.save()
        project0 = self.exampleProject()
        project0.save()
        return Enrollment(user=user0, course=course0, semester=semester0, meeting_days="MWR",
                          meeting_start_time="09:00", meeting_end_time="12:00", project=project0,
                          is_active=1, crn="12345")

    # simple put request for Record
    def test_basic_put(self):
        enrollment0 = self.exampleEnrollment()
        enrollment0.save()
        project0_id = enrollment0.project.id
        category0 = self.exampleCategory()
        category0.save()
        # create a basic record
        record = self.client.post('/record/',
                                  {
                                      'enrollment': enrollment0.id,
                                      'project': project0_id,
                                      'date': "2016-11-27",
                                      'start_time': "08:00:00",
                                      'total_hours': 4.5,
                                      'longitude': 42.3399,
                                      'latitude': 71.0891,
                                      'category': category0.name,
                                      'is_active': True,
                                      'comments': "Comments",
                                      'extra_field': None
                                  })
        record_json_string = json.loads(record.content.decode('utf-8'))
        self.assertEqual(record.status_code, 200)
        self.assertTrue(record_json_string['is_active'])

        new_info = {
	    'enrollment': enrollment0.id,
	    'project': project0_id,
	    'date': "2016-11-27",
	    'start_time': "08:00:00",
	    'total_hours': 6,
	    'longitude': 42.3399,
	    'latitude': 71.0891,
	    'category': category0.name,
	    'is_active': True,
	    'comments': "Comments",
	    'extra_field': None
        }

        # update record
        record2 = self.client.put('/record/%d/' % record_json_string['id'], json.dumps(new_info), content_type="application/json")
        record2_json_string = json.loads(record2.content.decode('utf-8'))
        self.assertEqual(record.status_code, 200)
        self.assertNotEqual(record_json_string['id'], record2_json_string['id'])
        self.assertEqual(record_json_string['enrollment'], record2_json_string['enrollment'])
        self.assertEqual(record_json_string['project'], record2_json_string['project'])
        self.assertEqual(record_json_string['date'], record2_json_string['date'])
        self.assertEqual(record_json_string['start_time'], record2_json_string['start_time'])
        self.assertNotEqual(record_json_string['total_hours'], record2_json_string['total_hours'])
        self.assertEqual(record_json_string['longitude'], record2_json_string['longitude'])
        self.assertEqual(record_json_string['latitude'], record2_json_string['latitude'])
        self.assertEqual(record_json_string['category'], record2_json_string['category'])
        self.assertEqual(record_json_string['comments'], record2_json_string['comments'])
        self.assertEqual(record_json_string['extra_field'], str(record2_json_string['extra_field']))
        self.assertFalse(Record.objects.get(pk=record_json_string['id']).is_active)

    # invalid put request --> update non-is_update field
    def test_invalid_put(self):
        enrollment0 = self.exampleEnrollment()
        enrollment0.save()
        project0_id = enrollment0.project.id
        category0 = self.exampleCategory()
        category0.save()
        # create a basic record
        record = self.client.post('/record/',
                                  {
                                      'enrollment': enrollment0.id,
                                      'project': project0_id,
                                      'date': "2016-11-27",
                                      'start_time': "08:00:00",
                                      'total_hours': 4.5,
                                      'longitude': 42.3399,
                                      'latitude': 71.0891,
                                      'category': category0.name,
                                      'is_active': True,
                                      'comments': "Comments",
                                      'extra_field': None
                                  })
        record_json_string = json.loads(record.content.decode('utf-8'))
        self.assertEqual(record.status_code, 200)
        self.assertTrue(record_json_string['is_active'])

        new_info = {
	    'enrollment': enrollment0.id,
	    'project': project0_id,
	    'date': "2016-11-27",
	    'start_time': "08:00:00",
            'total_hours': -10,
	    'longitude': 42.3399,
	    'latitude': 71.0891,
	    'category': category0.name,
	    'is_active': False,
	    'comments': "Comments",
	    'extra_field': None
        }

        # update record
        record = self.client.put('/record/%d/' % record_json_string['id'], json.dumps(new_info), content_type="application/json")
        self.assertEqual(record.status_code, 400)

        new_info = {
	    'enrollment': enrollment0.id,
	    'project': project0_id,
	    'date': "2016-11-27",
	    'start_time': "08:00:00",
            'total_hours': -10,
	    'longitude': 42.3399,
	    'latitude': 71.0891,
	    'category': category0.name,
	    'is_active': False,
	    'comments': "Comments",
	    'extra_field': None
        }
        # update record
        record = self.client.put('/record/%s/' % "99999", json.dumps(new_info), content_type="application/json")
        self.assertEqual(record.status_code, 404)
