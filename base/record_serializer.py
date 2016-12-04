from base.models import Record
from rest_framework import serializers
from base.record_category_serializer import RecordCategorySerializer


class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = ('id', 'enrollment', 'project', 'date', 'start_time', 'total_hours', 'longitude', 'latitude',
                  'category', 'is_active', 'comments', 'extra_field')

    def validate(self, data):
        if ('latitude' in data and 'longitude' not in data) or ('latitude' not in data and 'longitude' in data):
            raise serializers.ValidationError("Need to provide both longitude and latitude or neither!")
        return data
