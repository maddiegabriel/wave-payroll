from rest_framework import serializers
from .models import TimeLog, JobGroup
from django.core.validators import MinValueValidator
import datetime

class TimeLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeLog
        fields = ['employee_id', 'date_worked', 'hours_worked', 'job_group']

    def create(self, validated_data):
        """
        Create and return a new `TimeLog` instance, given the validated data.
        """
        return TimeLog.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `TimeLog` instance, given the validated data.
        """
        instance.employee_id = validated_data.get('employee_id', instance.employee_id)
        instance.date_worked = validated_data.get('date_worked', date_worked.date_worked)
        instance.hours_worked = validated_data.get('hours_worked', instance.hours_worked)
        instance.job_group = validated_data.get('job_group', instance.job_group)
        instance.save()
        return instance