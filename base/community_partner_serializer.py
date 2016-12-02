from base.models import CommunityPartner
from django.contrib.auth.models import User
from rest_framework import serializers

class CommunityPartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityPartner
        fields = ('id', 'name')
