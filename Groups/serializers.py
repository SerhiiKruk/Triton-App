from rest_framework.serializers import ModelSerializer
from .models import Group, Student

class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = ['name', 'faculty']

class StudentSerializer(ModelSerializer):
    class Meta:
        model = Student
        fields = ['first_name', 'second_name', 'photo', 'group_id']

