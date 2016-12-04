from django.test import TestCase
from django.test import Client
from base.models import Course, Department, College, CommunityPartner, Project, Enrollment, Semester
from django.contrib.auth.models import User
import json
from datetime import datetime

class EnrollmentTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.college = College("hello")
        self.college.save()
        self.department = Department("test", self.college.name)
        self.department.save()
        self.course = Course("CS4500", "Software Dev", self.department.name)
        self.course.save()
        self.user = User(username="ek@neu.edu", email="ek@neu.edu", password="password1")
        self.user.save()
        self.semester = Semester(name="sem", start_date=datetime.now(), end_date=datetime.now(), is_active=True)
        self.semester.save()

    def test_good_get(self):
        enrollment = Enrollment(user=self.user, course=self.course, semester=self.semester, meeting_days="MWF", meeting_start_time=datetime.now().time(), meeting_end_time=datetime.now().time(), crn="12345")
        enrollment.save()
        get_enrollment = self.client.get('/enroll/' + str(enrollment.id) + '/')
        self.assertEqual(get_enrollment.status_code, 200)
        json_string = json.loads(get_enrollment.content.decode('utf-8'))
        self.assertEqual(json_string['is_active'], True)
        self.assertEqual(json_string['meeting_days'], enrollment.meeting_days)

    def test_bad_get(self):
        get_enrollment = self.client.get('/enroll/1337/')
        self.assertEqual(get_enrollment.status_code, 404)

    def test_good_post(self):
        post_enrollment = self.client.post('/enroll/',
        {
            "user": self.user.id,
            "course": self.course.id,
            "semester": self.semester.name,
            "meeting_days": "MWF",
            "meeting_start_time": str(datetime.now().time()),
            "meeting_end_time": str(datetime.now().time()),
            "crn": "12345"
        })
        self.assertEqual(post_enrollment.status_code, 201)

    def test_bad_post_no_crn(self):
        post_enrollment = self.client.post('/enroll/',
        {
            "user": self.user.id,
            "course": self.course.id,
            "semester": self.semester.name,
            "meeting_days": "MWF",
            "meeting_start_time": str(datetime.now().time()),
            "meeting_end_time": str(datetime.now().time())
        })
        self.assertEqual(post_enrollment.status_code, 400)

    def test_bad_post_no_meeting_times(self):
        post_enrollment = self.client.post('/enroll/',
        {
            "user": self.user.id,
            "course": self.course.id,
            "semester": self.semester.name,
            "crn": "12345"
        })
        self.assertEqual(post_enrollment.status_code, 400)

    def test_good_put(self):
        enrollment = Enrollment(user=self.user, course=self.course, semester=self.semester, meeting_days="MWF", meeting_start_time=datetime.now().time(), meeting_end_time=datetime.now().time(), crn="12345")
        enrollment.save()
        temp_dict = {
            "crn": "98765"
        }
        put_enrollment = self.client.put('/enroll/' + str(enrollment.id) + '/', json.dumps(temp_dict), content_type="application/json")
        self.assertEqual(put_enrollment.status_code, 200)
        enrollment.refresh_from_db()
        self.assertEqual(enrollment.crn, "98765")

    def test_bad_put(self):
        enrollment = Enrollment(user=self.user, course=self.course, semester=self.semester, meeting_days="MWF", meeting_start_time=datetime.now().time(), meeting_end_time=datetime.now().time(), crn="12345")
        enrollment.save()
        temp_dict = {
            "user": "Hi There"
        }
        put_enrollment = self.client.put('/enroll/' + str(enrollment.id) + '/', json.dumps(temp_dict), content_type="application/json")
        self.assertEqual(put_enrollment.status_code, 400)

    def test_delete(self):
        enrollment = Enrollment(user=self.user, course=self.course, semester=self.semester, meeting_days="MWF", meeting_start_time=datetime.now().time(), meeting_end_time=datetime.now().time(), crn="12345")
        enrollment.save()
        delete_enrollment = self.client.delete('/enroll/' + str(enrollment.id) + '/')
        self.assertEqual(delete_enrollment.status_code, 204)
        get_enrollment = self.client.get('/enroll/' + str(enrollment.id) + '/')
        self.assertEqual(get_enrollment.status_code, 404)

    def test_get_all(self):
        enrollment = Enrollment(user=self.user, course=self.course, semester=self.semester, meeting_days="MWF", meeting_start_time=datetime.now().time(), meeting_end_time=datetime.now().time(), crn="12345")
        enrollment.save()
        get_enrollments = self.client.get('/enrollments/')
        self.assertEqual(get_enrollments.status_code, 200)
        json_string = json.loads(get_enrollments.content.decode('utf-8'))
        self.assertEqual(json_string[0]['is_active'], True)

    def test_get_all_for_course(self):
        enrollment = Enrollment(user=self.user, course=self.course, semester=self.semester, meeting_days="MWF", meeting_start_time=datetime.now().time(), meeting_end_time=datetime.now().time(), crn="12345")
        enrollment.save()
        get_enrollments = self.client.get('/enrollments/' + self.course.id + '/')
        self.assertEqual(get_enrollments.status_code, 200)
        json_string = json.loads(get_enrollments.content.decode('utf-8'))
        self.assertEqual(json_string[0]['is_active'], True)

    def test_get_all_for_crn(self):
        enrollment = Enrollment(user=self.user, course=self.course, semester=self.semester, meeting_days="MWF", meeting_start_time=datetime.now().time(), meeting_end_time=datetime.now().time(), crn="12345")
        enrollment.save()
        get_enrollments = self.client.get('/enrollments/crn/' + enrollment.crn + '/')
        self.assertEqual(get_enrollments.status_code, 200)
        json_string = json.loads(get_enrollments.content.decode('utf-8'))
        self.assertEqual(json_string[0]['is_active'], True)
