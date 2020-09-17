from django.core.validators import RegexValidator
from django.shortcuts import reverse
from django.db import models
from django.utils.text import slugify
from time import time

def gen_slug(s):
    new_slug = slugify(s, allow_unicode=True)
    return new_slug + "-" + str(int(time()))

class Group(models.Model):
    name = models.CharField(max_length=40, unique=True)
    faculty = models.CharField(max_length=25)
    slug = models.SlugField(max_length=150, unique=True)
    course = models.IntegerField()
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('group_detail', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('group_update', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('group_delete', kwargs={'slug': self.slug})

class Mark(models.Model):
    class Type(models.TextChoices):
        Exam = "Exam"
        Test = "Test"
    class Semester(models.IntegerChoices):
        First = 1
        Second = 2
    mark = models.IntegerField()
    subject = models.ForeignKey('Subject',  on_delete=models.CASCADE)
    type = models.CharField(choices=Type.choices, max_length=10)
    semester = models.IntegerField(choices=Semester.choices)
    date = models.DateField(auto_now_add=False, auto_now=False)

    #def get_update_url(self):
     #   return reverse('mark_update', kwargs={'id': self.id})

   # def get_delete_url(self):
    #    return reverse('mark_delete', kwargs={'id': self.id})


class Student(models.Model):
    first_name = models.CharField(max_length = 20)
    second_name = models.CharField(max_length = 20)
    date_of_birth = models.DateField(auto_now_add=False, auto_now=False)
    slug = models.SlugField(max_length=150, unique=True)
    photo = models.ImageField(blank=False)
    group_id = models.ForeignKey('Group', related_name='students', on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    marks = models.ManyToManyField('Mark')
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.second_name)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.first_name+self.second_name)
            group = self.group_id
            group.count = group.count + 1
            group.save()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('student_detail', kwargs={'slug':self.slug})

    def get_update_url(self):
        return reverse('student_update', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('student_delete', kwargs={'slug': self.slug})

    def get_marks_url(self):
        return reverse('marks_list', kwargs={'slug': self.slug})

class Subject(models.Model):
    name = models.CharField(max_length=25, unique=True)
    info = models.TextField()

    def __str__(self):
        return '{}'.format(self.name)

class Lesson(models.Model):
    class Type(models.TextChoices):
        Lecture = "Lecture"
        Practice = "Practice"
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
    type = models.TextField(Type.choices)
    teacher = models.TextField(max_length=100)




