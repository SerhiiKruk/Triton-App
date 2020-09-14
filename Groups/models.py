from django.shortcuts import reverse
from django.db import models
from django.utils.text import slugify
from time import time

def gen_slug(s):
    new_slug = slugify(s, allow_unicode=True)
    return new_slug + "-" + str(int(time()))

class Group(models.Model):
    name = models.CharField(max_length=40, unique=True)
    faculty = models.CharField(max_length=40)
    slug = models.SlugField(max_length=150, unique=True)

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

class Student(models.Model):
    first_name = models.CharField(max_length = 20)
    second_name = models.CharField(max_length = 20)
    slug = models.SlugField(max_length=150, unique=True)
    photo = models.ImageField(blank=False)
    group_id = models.ForeignKey('Group', related_name='students', on_delete=models.CASCADE)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.second_name)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.first_name+self.second_name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('student_detail', kwargs={'slug':self.slug})

    def get_update_url(self):
        return reverse('student_update', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('student_delete', kwargs={'slug': self.slug})
