import base64
import io

from PIL import Image
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.views import View, generic
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .models import Group, Student, Mark, Subject
from .forms import GroupForm, StudentForm, MarkForm

from rest_framework.viewsets import ModelViewSet
from .serializers import GroupSerializer, StudentSerializer, SubjectSerializer
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

# def any(request):
#     return render(request, 'Groups/test1.html')
#
# def stat(request, slug):
#     list = []
#     group = Group.objects.get(slug=slug)
#     list_stud = Student.objects.filter(group_id=group)
#     for student in list_stud:
#         count = student.marks.count()
#         sum = 0
#         for mark in student.marks.all():
#             sum += mark.mark
#         avg = sum / count
#         data = {
#             "student":"{} {}".format(student.first_name, student.second_name),
#             "avg": avg
#         }
#         list.append(data)
#     return JsonResponse(list, safe=False)

def home_page(request):
    return render(request, 'Groups/home_page.html')

class GroupsList(View):
    def get(self, request):
        search_query = request.GET.get('search', '')

        if (search_query):
            groups = Group.objects.filter(Q(name__icontains=search_query)).order_by('name')
            search = '&search={}'.format(search_query)
        else:
            groups = Group.objects.all().order_by('name')
            search = ''

        context = get_context_pagintaion(request, groups, search)
        return render(request, 'Groups/groups_list.html', context={'context': context})

class StudentsList(View):
    def get(self, request):
        search_query = request.GET.get('search', '')

        if(search_query):
            students = Student.objects.filter(Q(first_name__icontains=search_query)
                                              or Q(second_name__icontains=search_query)).order_by('second_name')
            search = '&search={}'.format(search_query)
        else:
            students = Student.objects.all().order_by('second_name')
            search = ''
        context = get_context_pagintaion(request, students, search)
        return render(request, 'Groups/students_list.html', context={'context': context})

# Pagination
def get_context_pagintaion(request, objects, search):
    paginator = Paginator(objects, 10)
    page_number = request.GET.get('page', 1)

    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page_number = 1
        page = paginator.page(page_number)
    except EmptyPage:
        page_number = 1
        page = paginator.page(page_number)

    is_paginated = page.has_other_pages()

    if page.has_previous():
        prev_url = '?page={}'.format(page.previous_page_number()) + search
    else:
        prev_url = ''

    if page.has_next():
        next_url = '?page={}'.format(page.next_page_number()) + search
    else:
        next_url = ''

    context = {
        'page_object': page,
        'page_number': page_number,
        'is_paginated': is_paginated,
        'next_url': next_url,
        'prev_url': prev_url,
    }
    return context
# end pagination

class StudentDetail(View):
    def get(self, request, slug):
        student = get_object_or_404(Student, slug__iexact=slug)
        return render(request, 'Groups/student_detail.html',context={'student':student})

class GroupDetail(View):
    def get(self, request, slug):
        group = get_object_or_404(Group, slug__iexact=slug)
        students = Student.objects.filter(group_id=group)
        return render(request, 'Groups/group_detail.html', context={'students': students, 'group': group})

class GroupMap(View):
    def get(self, request, slug):
        group = Group.objects.get(slug=slug)
        students = Student.objects.filter(group_id=group)
        return render(request, 'Groups/group_map.html', context={'students': students})

class GroupCreate(View):
    def get(self, request):
       form = GroupForm()
       return render(request, 'Groups/group_create.html', context={'form': form})

    def post(self, request):
        bound_form = GroupForm(request.POST)

        if bound_form.is_valid():
            new_group = bound_form.save()
            return redirect('groups_list')
        return render(request, 'Groups/group_create.html', context={'form': bound_form})

class StudentCreate(View):
    def get(self, request):
        form = StudentForm()
        return render(request, 'Groups/student_create.html', context={'form': form})

    def post(self, request):
        bound_form = StudentForm(request.POST, request.FILES)
        if bound_form.is_valid():
            new_student = bound_form.save()
            return redirect('students_list')
        return render(request, 'Groups/student_create.html', context={'form': bound_form})

class GroupUpdate(View):
    def get(self, request, slug):
        group = Group.objects.get(slug__iexact=slug)
        bound_form = GroupForm(instance=group)
        return render(request, 'Groups/group_update.html', context={'form': bound_form, 'group': group})

    def post(self, request, slug):
        group = Group.objects.get(slug__iexact=slug)
        bound_form = GroupForm(request.POST, instance=group)

        if bound_form.is_valid():
            new_group = bound_form.save()
            return redirect(new_group)
        return render(request, 'Groups/group_update.html', context = {'form':bound_form, 'group':group})

class StudentUpdate(View):
    def get(self, request, slug):
        student = Student.objects.get(slug__iexact=slug)
        bound_form = StudentForm(instance=student)
        return render(request, 'Groups/student_update.html', context={'form': bound_form, 'student': student})

    def post(self, request, slug):
        student = Student.objects.get(slug__iexact=slug)
        prev_group = student.group_id
        bound_form = StudentForm(request.POST, request.FILES, instance=student)

        if bound_form.is_valid():
            prev_group.count -= 1;
            prev_group.save()
            new_student = bound_form.save()
            new_group = new_student.group_id
            new_group.count += 1
            new_group.save()
            return redirect(new_student)
        return render(request, 'Groups/student_update.html', context = {'form':bound_form, 'student':student})

class GroupDelete(View):
    def get(self, request, slug):
        group = Group.objects.get(slug__iexact = slug)
        return render(request, 'Groups/group_delete.html', context = {'group': group})

    def post(self, request, slug):
        group = Group.objects.get(slug__iexact=slug)
        group.delete()
        return redirect('groups_list')

class StudentDelete(View):
    def get(self, request, slug):
        student = Student.objects.get(slug__iexact = slug)
        return render(request, 'Groups/student_delete.html', context = {'student': student})

    def post(self, request, slug):
        student = Student.objects.get(slug__iexact=slug)
        group = student.group_id
        group.count = group.count - 1
        group.save()
        student.delete()
        return redirect('students_list')

class MarkList(View):
    def get(self, request, slug):
        student = Student.objects.get(slug=slug)
        return render(request, 'Groups/marks_list.html', context={'student': student})

class MarkCreate(View):
    def get(self, request, slug):
        form = MarkForm()
        return render(request, 'Groups/mark_create.html', context={'form': form, 'slug': slug})

    def post(self, request, slug):
        bound_form = MarkForm(request.POST)

        if bound_form.is_valid():
            new_mark = bound_form.save()
            student = Student.objects.get(slug=slug)
            student.marks.add(new_mark)
            return redirect('marks_list', student.slug)
        return render(request, 'Groups/mark_create.html', context={'form': bound_form, 'slug': slug})

class MarkUpdate(View):
    def get(self, request, slug, id):
        mark = Mark.objects.get(id__iexact=id)
        bound_form = MarkForm(instance=mark)
        return render(request, 'Groups/mark_update.html', context={'form': bound_form, 'slug': slug, 'id': id})

    def post(self, request, slug, id):
        mark = Mark.objects.get(id__iexact=id)
        bound_form = MarkForm(request.POST, instance=mark)

        if bound_form.is_valid():
            new_mark = bound_form.save()
            return redirect('marks_list', slug)
        return render(request, 'Groups/mark_update.html', context={'form': bound_form, 'slug': slug, 'id': id})

class MarkDelete(View):
    def get(self, request, slug, id):
        mark = Mark.objects.get(id__iexact=id)
        return render(request, 'Groups/mark_delete.html', context={'mark': mark, 'slug': slug, 'id': id})

    def post(self, request, slug, id):
        mark = Mark.objects.get(id__iexact=id)
        mark.delete()
        return redirect('marks_list', slug)


######## WEB API ################3
## for students

class StudentsView(ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def perform_create(self, serializer):
        group = get_object_or_404(Group, id=self.request.data.get('group_id'))
        return serializer.save(group_id=group)

class SingleStudentView(RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class GroupsView(ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def perform_create(self, serializer):
        return serializer.save()

class SingleGroupView(RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class SubjectsView(ListCreateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

    def perform_create(self, serializer):
        return serializer.save()

class SingleSubjectView(RetrieveUpdateDestroyAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer




