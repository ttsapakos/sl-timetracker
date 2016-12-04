from base.models import Course, Project, Enrollment, UserProfile, User
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_auth.serializers import UserDetailsSerializer
from django.http import Http404
from base.course_serializer import CourseSerializer
from base.project_serializer import ProjectSerializer
from base.user_serializer import UserSerializer
from base.enrollment_serializer import SectionSerializer

class CourseDetail(APIView):
    def get_object(self, pk):
        try:
            return Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            raise Http404("Object doesn't exist")

    def get(self, request, pk, format=None):
        course = self.get_object(pk)
        course = CourseSerializer(course)
        return Response(course.data)

    def post(self, request, format=None):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CourseList(APIView):
    def get(self, request, format=None):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

class CourseProjectList(APIView):
    def get(self, request, course, format=None):
        projects = Project.objects.filter(course=course)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

class CourseInstructorList(APIView):
    def get(self, request, course, format=None):
        instructors = User.objects.filter(id__in=Enrollment.objects.filter(course=course, user__userprofile__role=UserProfile.INSTRUCTOR).values_list('user', flat=True))
        serializer = UserSerializer(instructors, many=True)
        return Response(serializer.data)

class CourseStudentList(APIView):
    def get(self, request, course, format=None):
        students = User.objects.filter(id__in=Enrollment.objects.filter(course=course, user__userprofile__role=UserProfile.STUDENT).values_list('user', flat=True))
        serializer = UserSerializer(students, many=True)
        return Response(serializer.data)

class CourseSectionsList(APIView):
    def get(self, request, course, format=None):
        enrollments = Enrollment.objects.filter(id__in=Enrollment.objects.filter(course=course, user__userprofile__role=UserProfile.INSTRUCTOR).values('crn').distinct().values('id'))
        serializer = SectionSerializer(enrollments, many=True)
        return Response(serializer.data)
