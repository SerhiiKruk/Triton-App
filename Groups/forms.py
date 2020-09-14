from re import match

from django import forms
from .models import Group, Student
from django.core.exceptions import ValidationError

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'faculty']

        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'faculty': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_faculty(self):
        new_faculty = self.cleaned_data['faculty']
        pattern = r'^[A-Z][a-z]+'
        res = match(pattern, new_faculty)
        if res is None:
            raise ValidationError('Wrong faculty')
        return new_faculty

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'second_name', 'photo', 'group_id']

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'second_name': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'group_id': forms.Select(attrs={'class': 'form-control'}),
                    }

    def clean_first_name(self):
        new_first_name = self.cleaned_data['first_name']
        pattern = r'^[A-Z][a-z]+'
        res = match(pattern, new_first_name)
        if res is None:
            raise ValidationError('Wrong first name')
        return new_first_name

    def clean_second_name(self):
        new_second_name = self.cleaned_data['second_name']
        pattern = r'^[A-Z][a-z]+'
        res = match(pattern, new_second_name)
        if res is None:
            raise ValidationError('Wrong second name')
        return new_second_name
