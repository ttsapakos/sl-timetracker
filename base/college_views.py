from base.models import College
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from base.college_serializer import CollegeSerializer

class CollegeDetail(APIView):
    def get_object(self, pk):
        try:
            return College.objects.get(pk=pk)
        except College.DoesNotExist:
            raise Http404("Object doesn't exist")

    def get(self, request, pk, format=None):
        college = self.get_object(pk)
        college = CollegeSerializer(college)
        return Response(college.data)

    def post(self, request, format=None):
        serializer = CollegeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        college = self.get_object(pk)
        serializer = CollegeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            college.delete()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        college = self.get_object(pk)
        college.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CollegeList(APIView):
    def get(self, request, format=None):
        colleges = College.objects.all()
        serializer = CollegeSerializer(colleges, many=True)
        return Response(serializer.data)
