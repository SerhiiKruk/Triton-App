from re import match

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Group, Student, Subject


class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = ['name', 'faculty', 'course']

class StudentSerializer(ModelSerializer):
    def validate(self, data):
        errors = {}
        first_name = data.get('first_name')
        second_name = data.get('second_name')
        len1 = len(first_name)
        len2 = len(second_name)
        pattern = r'^[A-Z][a-z]+'
        res = match(pattern, first_name)
        if res is None or len1 != res.span()[1]:
            errors['error'] = 'First_name should begin with capital letter and do not contain numbers and symbols'
            raise serializers.ValidationError(errors)
        res = match(pattern, first_name)
        if res is None or len2 != res.span()[1]:
            errors['error'] = 'Second_name should begin with capital letter and do not contain numbers and symbols'
            raise serializers.ValidationError(errors)
        return data

    class Meta:
        model = Student
        fields = ['first_name', 'second_name', 'photo', 'group_id', 'date_of_birth', 'phone_number', 'address','longitude', 'latitude']

class SubjectSerializer(ModelSerializer):
    class Meta:
        model = Subject
        fields = ['name', 'info']
