from django.test import TestCase
from django.test import Client
from base.models import Course, Department, College, CommunityPartner, Project, Enrollment, Semester
from django.contrib.auth.models import User
import json
from datetime import datetime

class CourseTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.college = College("hello")
        self.college.save()
        self.department = Department("test", self.college.name)
        self.department.save()

    def test_good_get(self):
        course = Course("CS4500", "Software Dev", self.department.name)
        course.save()
        get_course = self.client.get('/course/' + course.id + '/')
        self.assertEqual(get_course.status_code, 200)
        c_json_string = json.loads(get_course.content.decode('utf-8'))
        self.assertEqual(c_json_string['id'], course.id)
        self.assertEqual(c_json_string['name'], course.name)

    def test_bad_get(self):
        get_course = self.client.get('/course/FZ9999/')
        self.assertEqual(get_course.status_code, 404)

    def test_good_post(self):
        course = self.client.post('/course/',
        {
            "id": "CS4500",
            "name": "Software Dev",
            "department": self.department.name
        })
        self.assertEqual(course.status_code, 201)
        c_json_string = json.loads(course.content.decode('utf-8'))
        self.assertEqual(c_json_string['id'], "CS4500")
        self.assertEqual(c_json_string['name'], "Software Dev")
        self.assertEqual(c_json_string['department'], "test")

    def test_bad_post_no_id(self):
        course = self.client.post('/course/',
        {
            "name": "Software Dev",
            "department": self.department.name
        })
        self.assertEqual(course.status_code, 400)

    def test_bad_post_no_name(self):
        course = self.client.post('/course/',
        {
            "id": "CS4500",
            "department": self.department.name
        })
        self.assertEqual(course.status_code, 400)

    def test_bad_post_no_department(self):
        course = self.client.post('/course/',
        {
            "id": "CS4500",
            "name": "Software Dev"
        })
        self.assertEqual(course.status_code, 400)

    def test_get_all_courses(self):
        course = Course("CS4500", "Software Dev", self.department.name)
        course.save()
        get_courses = self.client.get('/courses/')
        self.assertEqual(get_courses.status_code, 200)
        c_json_string = json.loads(get_courses.content.decode('utf-8'))
        self.assertEqual(c_json_string[0]['id'], course.id)

    def test_get_all_course_projects(self):
        course = Course("CS4500", "Software Dev", self.department.name)
        course.save()
        community_partner = CommunityPartner(name="partner")
        community_partner.save()
        project = Project(name="project", course=course, community_partner=community_partner, start_date=datetime.now(), end_date=datetime.now())
        project.save()
        get_projects = self.client.get('/course/' + course.id + '/projects/')
        self.assertEqual(get_projects.status_code, 200)
        json_string = json.loads(get_projects.content.decode('utf-8'))
        self.assertEqual(json_string[0]['name'], project.name)

    def test_get_all_course_instructors(self):
        course = Course("CS4500", "Software Dev", self.department.name)
        course.save()
        user = User(username="ek@neu.edu", email="ek@neu.edu", password="password1")
        user.save()
        semester = Semester(name="sem", start_date=datetime.now(), end_date=datetime.now(), is_active=True)
        semester.save()
        enrollment = Enrollment(user=user, course=course, semester=semester, meeting_days="MWF", meeting_start_time=datetime.now().time(), meeting_end_time=datetime.now().time(), crn="12345")
        enrollment.save()
        get_instructors = self.client.get('/course/' + course.id + '/instructors/')
        self.assertEqual(get_instructors.status_code, 200)
        json_string = json.loads(get_instructors.content.decode('utf-8'))
        self.assertEqual(json_string[0]['email'], user.email)

    def test_get_all_course_students(self):
        course = Course("CS4500", "Software Dev", self.department.name)
        course.save()
        user = User(username="ek@husky.neu.edu", email="ek@husky.neu.edu", password="password1")
        user.save()
        semester = Semester(name="sem", start_date=datetime.now(), end_date=datetime.now(), is_active=True)
        semester.save()
        enrollment = Enrollment(user=user, course=course, semester=semester, meeting_days="MWF", meeting_start_time=datetime.now().time(), meeting_end_time=datetime.now().time(), crn="12345")
        enrollment.save()
        get_students = self.client.get('/course/' + course.id + '/students/')
        self.assertEqual(get_students.status_code, 200)
        json_string = json.loads(get_students.content.decode('utf-8'))
        self.assertEqual(json_string[0]['email'], user.email)

    def test_get_all_course_sections(self):
        course = Course("CS4500", "Software Dev", self.department.name)
        course.save()
        user = User(first_name="erik", last_name="kaasila", username="ek@neu.edu", email="ek@neu.edu", password="password1")
        user.save()
        semester = Semester(name="sem", start_date=datetime.now(), end_date=datetime.now(), is_active=True)
        semester.save()
        enrollment = Enrollment(user=user, course=course, semester=semester, meeting_days="MWF", meeting_start_time=datetime.now().time(), meeting_end_time=datetime.now().time(), crn="12345")
        enrollment.save()
        get_sections = self.client.get('/course/' + course.id + '/sections/')
        self.assertEqual(get_sections.status_code, 200)
        json_string = json.loads(get_sections.content.decode('utf-8'))
        self.assertEqual(json_string[0]['professor'], user.get_full_name())
