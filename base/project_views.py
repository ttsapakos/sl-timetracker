from base.models import *
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from base.project_serializer import ProjectSerializer
from base.user_serializer import UserSerializer

class ProjectDetail(APIView):
    """
    Post, retrieve, update or delete a project instance
    """
    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404("Object doesn't exist")

    def post(self, request, format=None):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk, format=None):
        project = self.get_object(pk)
        project = ProjectSerializer(project);
        return Response(project.data);

    def put(self, request, pk, format=None):
        project = self.get_object(pk)
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        project = self.get_object(pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProjectsAll(APIView):
    """
    Get all projects
    """
    def get(self, request, format=None):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

class ProjectStudents(APIView):
    """
    Get all students in a project
    """
    def get(self, request, pk, format=None):
        users = User.objects.filter(id__in=Enrollment.objects.filter(project=pk).values_list("user", flat=True))
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
