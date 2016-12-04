from base.models import Enrollment
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from base.enrollment_serializer import EnrollmentSerializer


class EnrollmentList(APIView):
    def get(self, request, format=None):
        enrollments = Enrollment.objects.all()
        serializer = EnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data)

class EnrollmentCourseList(APIView):
    def get(self, request, course, format=None):
        enrollments = Enrollment.objects.filter(course=course, is_active=True)
        serializer = EnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data)

class EnrollmentCRNList(APIView):
    def get(self, request, crn, format=None):
        enrollments = Enrollment.objects.filter(crn=crn, is_active=True)
        serializer = EnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data)

class EnrollmentDetail(APIView):
    def get_object(self, pk):
        try:
            return Enrollment.objects.get(pk=pk)
        except Enrollment.DoesNotExist:
            raise Http404("Object doesn't exist")

    def get(self, request, pk, format=None):
        enrollment = self.get_object(pk)
        enrollment = EnrollmentSerializer(enrollment)
        return Response(enrollment.data)

    def post(self, request, format=None):
        serializer = EnrollmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        enrollment = self.get_object(pk)
        serializer = EnrollmentSerializer(enrollment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        enrollment = self.get_object(pk)
        enrollment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
