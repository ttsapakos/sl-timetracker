from base.models import Semester
from rest_framework import serializers

class SemesterSerializer(serializers.ModelSerializer):	
    class Meta:
	    model = Semester
	    fields = ('name', 'start_date', 'end_date', 'is_active',)
