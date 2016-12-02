from base.models import Project
from django.contrib.auth.models import User
from rest_framework import serializers
from base.community_partner_serializer import CommunityPartnerSerializer

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'name', 'course', 'community_partner', 'description', 'start_date', 'end_date', 'longitude', 'latitude')
