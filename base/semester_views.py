from django.http import Http404
from django.db.models import Sum
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status

from base.semester_serializer import SemesterSerializer

from base.models import Semester, Enrollment
import datetime
class SemesterDetail(generics.ListCreateAPIView):

	""" API Endpoint for Semesters
	POST - Create a semester
	GET - Get info on a semester for a given semester idi
	PUT - Update info on a semester, given its name
	"""

	def get_object(self, pk):
		try:
			return Semester.objects.get(pk=pk)
		except Semester.DoesNotExist:
			raise Http404("Object doesn't exist")

	def get(
		self,
		request,
		pk,
		format=None,
		):
		semester = self.get_object(pk)
		serializer = SemesterSerializer(semester)
		return Response(serializer.data)

	def post(self, request, format=None):
		serializer = SemesterSerializer(data=request.data)
		if serializer.is_valid():
			if (request.data['start_date'] < request.data['end_date']):
				serializer.save()
				return Response(serializer.data, status=status.HTTP_201_CREATED)
			else:
				return Response('Malformed date(s)', status=status.HTTP_400_BAD_REQUEST)
		return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
	
	def put(
		self,
		request,
		pk,
		format=None,
		):
		semester = self.get_object(pk)
		serializer = SemesterSerializer(semester, data=request.data)
		if serializer.is_valid():
			if (request.data['start_date'] < request.data['end_date']):
				serializer.save()
				return Response(serializer.data)
			else:
				return Response('Malformed date(s)', status.HTTP_400_BAD_REQUEST)
		return Response(serializer.errors,
						status=status.HTTP_400_BAD_REQUEST)


class StartSemester(generics.CreateAPIView):

	def post(
		self,
		request,
		format=None,
		):
		###permission_classes = (permissions.IsAuthenticated, )
		if True: #request.user.is_superuser:
			current = Semester.objects.get(is_active=True)
			Enrollment.objects.filter(semester=current).update(is_active=False)
			coming_up = Semester.objects.filter(is_active=False).filter(start_date__gt=datetime.date.today()).exclude(name=current).order_by('start_date')
			try:
				next_selection = coming_up[0]
				next_selection.is_active = True
				next_selection.save()
			except IndexError:
				raise Http404("No next semester available")
			Enrollment.objects.filter(semester=next_selection).update(is_active=True)
			for person in User.objects.all():
				actives = Enrollment.objects.filter(user_id=person.id).aggregate(sum=Sum('is_active'))['sum']				
				if actives == 0:
					person.is_active=False
				else:
					person.is_active=True
				person.save()
			current.is_active = False
			current.save()
			return Response(status=status.HTTP_200_OK)
		else:
			return Response(status=status.HTTP_403_FORBIDDEN)
