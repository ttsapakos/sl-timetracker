from base.models import RecordCategory
from rest_framework import serializers


class RecordCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RecordCategory
        fields = ('name', 'description')
