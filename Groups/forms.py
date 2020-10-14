from re import match

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Group, Student, Mark, Profile
from django.core.exceptions import ValidationError

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'faculty', 'course']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'faculty': forms.TextInput(attrs={'class': 'form-control'}),
            'course': forms.TextInput(attrs={'class': 'form-control'})
        }

    def clean_course(self):
        new_course = self.cleaned_data['course']
        if(new_course<0 or new_course>6):
            return ValidationError('No such course. Choose 1-6')
        return new_course

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
        fields = ['first_name', 'second_name', 'photo', 'group_id', 'date_of_birth', 'phone_number', 'address', 'latitude', 'longitude']

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'second_name': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'group_id': forms.Select(attrs={'class': 'form-control', 'name': 'group'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'longitude': forms.TextInput(attrs={'class': 'form-control'}),
            'latitude': forms.TextInput(attrs={'class': 'form-control'}),
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

class MarkForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = ['subject', 'type', 'semester', 'date', 'mark']

        widgets = {
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'semester': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control'}),
            'mark': forms.TextInput(attrs={'class': 'form-control'}),
                  }

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['favorite_lang', 'student']

    # widgets = {
    #     'student': forms.Select(attrs={'class': 'form-control'})
    # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['student'].queryset = Student.objects.none()

        if 'student' in self.data:
            self.fields['student'].queryset = Student.objects.all()

        elif self.instance.id:
            self.fields['student'].queryset = Student.objects.get(id=self.instance.student.id)

