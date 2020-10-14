import json

from django.contrib import auth, messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Group, Student, Mark, Subject
from .forms import GroupForm, StudentForm, MarkForm, ProfileForm, RegisterForm
from .serializers import GroupSerializer, StudentSerializer, SubjectSerializer
from .tokens import account_activation_token


def home_page(request):
    return render(request, 'Groups/home_page.html')

@login_required
def profile(request):
    if request.user.profile is not None:
        student = request.user.profile.student
        return render(request, 'Groups/profile.html', {'student': student})
    else:
        redirect('profile_add')

@login_required
def profile_add(request):
    if request.is_ajax():
        students = Student.objects.all().filter(is_registered=False, second_name__istartswith=request.GET.get('term'))
        response_content = list(students.values())
        return JsonResponse(response_content, safe=False)
    else:
        if request.method == "GET":
            form = ProfileForm()
            return render(request, 'Groups/profile_add.html', context={'form': form})
        elif request.method == "POST":
            profile_form = ProfileForm(request.POST)
            if profile_form.is_valid():
                user = request.user
                user.refresh_from_db()
                profile_form = ProfileForm(request.POST, instance=user.profile)
                profile = profile_form.save()
                user.first_name = profile.student.first_name
                user.last_name = profile.student.second_name
                user.save()
                user.profile.student.is_registered = True
                user.profile.student.save()
                return redirect('profile')
            return render(request, 'Groups/profile_add.html', context={'form': profile_form})

@login_required
def best_gpa(request):
    if request.user.is_active:
        request.user.refresh_from_db()
        if request.user.profile is not None:
            group = request.user.profile.student.group_id
            data = Student.objects.filter(group_id=group) \
            .values('first_name', 'second_name', 'avg_mark') \
            .order_by('-avg_mark')[:10]

            categories = list()
            series = list()

            for entry in data:
                categories.append('{} {}'.format(entry['first_name'], entry['second_name']))
                series.append(entry['avg_mark'])

            chart = {
                'chart': {'type': 'bar'},
                'title': {'text': 'Top-10 GPA in your group'},
                'xAxis': {'categories': categories},
                'yAxis': {
                    'min': 60,
                    'max': 100,
                    'title': {
                        'align': 'high'
                    },
                    'labels': {
                        'overflow': 'justify'
                    }
                },
                'series': [{
                    'name': 'GPA',
                    'data': series,
                    'color': 'blue'
                }]
            }

            dump = json.dumps(chart)

            return render(request, 'Groups/gpa_best.html', {'chart': dump})
        else:
            return redirect('profile_add')
    else:
        return redirect('signin_url')


def account_activation_sent(request):
    return render(request, 'Groups/account_activation_sent.html')

def signup(request):
    if request.method == 'POST':
        user_form = RegisterForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            user.refresh_from_db()
            profile_form = ProfileForm(request.POST, instance=user.profile)
            profile_form.full_clean()
            profile = profile_form.save()

            user.first_name = profile.student.first_name
            user.last_name = profile.student.second_name
            profile.student.is_registered = True
            profile.student.save()
            user.save()
            mail_subject = 'Activate your StepUnder account.'
            message = render_to_string('Groups/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = profile_form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return render(request, 'Groups/confirm_email.html', {'message': 'Please, confirm your email in order to login'})
    else:
        user_form = RegisterForm()
        profile_form = ProfileForm()
    return render(request, 'Groups/signup.html', {'user_form': user_form, 'profile_form': profile_form})


def signin(request):
    if request.user.is_active:
        return redirect('home_page')

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is None:
            messages.info(request, 'Account with such password and username does not exist')
            return render(request, 'Groups/signin.html')
        else:
            auth.login(request, user)
            return redirect('home_page')
    else:
        return render(request, 'Groups/signin.html')

@login_required
def signout(request):
    if request.method == "GET":
        return render(request, 'Groups/signout.html')
    else:
        auth.logout(request)
        return redirect('home_page')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('home_page')
    else:
        return render(request, 'Groups/confirm_email.html', {'message': 'Invalid token'})

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
        if request.user.is_superuser:
            student = get_object_or_404(Student, slug__iexact=slug)
            labels = ['3', '4', '5']
            data = []
            marks_enough = student.marks.filter(mark__gt=59, mark__lt=75).count()
            marks_good = student.marks.filter(mark__gt=75, mark__lt=90).count()
            marks_excellent = student.marks.filter(mark__gt=89).count()

            data.append(marks_enough)
            data.append(marks_good)
            data.append(marks_excellent)

            return render(request, 'Groups/student_detail.html', context={'student': student, 'labels':labels, 'data':data})
        else:
            return render(request, 'Groups/permission_page.html')

class GroupDetail(View):
    def get(self, request, slug):
        if request.user.is_superuser:
            group = get_object_or_404(Group, slug__iexact=slug)
            students = Student.objects.filter(group_id=group)
            return render(request, 'Groups/group_detail.html', context={'students': students, 'group': group})
        else:
            return render(request, 'Groups/permission_page.html')

class GroupMap(View):
    def get(self, request, slug):
        if request.user.is_superuser:
            group = Group.objects.get(slug=slug)
            students = Student.objects.filter(group_id=group)
            return render(request, 'Groups/group_map.html', context={'students': students})
        else:
            return render(request, 'Groups/permission_page.html')

class GroupCreate(View):
    def get(self, request):
       if request.user.is_superuser:
            form = GroupForm()
            return render(request, 'Groups/group_create.html', context={'form': form})
       else:
           return render(request, 'Groups/permission_page.html')

    def post(self, request):
            bound_form = GroupForm(request.POST)

            if bound_form.is_valid():
                new_group = bound_form.save()
                return redirect('groups_list')
            return render(request, 'Groups/group_create.html', context={'form': bound_form})

class StudentCreate(View):
    def get(self, request):
        if request.user.is_superuser:
            if request.is_ajax():
                groups = Group.objects.all().filter(name__istartswith=request.GET.get('term'))
                response_content = list(groups.values())
                return JsonResponse(response_content, safe=False)
            else:
                form = StudentForm()
                return render(request, 'Groups/student_create.html', context={'form': form})
        else:
            return render(request, 'Groups/permission_page.html')

    def post(self, request):
        bound_form = StudentForm(request.POST, request.FILES)
        if bound_form.is_valid():
            new_student = bound_form.save()
            return redirect('students_list')
        return render(request, 'Groups/student_create.html', context={'form': bound_form})

class GroupUpdate(View):
    def get(self, request, slug):
        if request.user.is_superuser:
            group = Group.objects.get(slug__iexact=slug)
            bound_form = GroupForm(instance=group)
            return render(request, 'Groups/group_update.html', context={'form': bound_form, 'group': group})
        else:
            return render(request, 'Groups/permission_page.html')

    def post(self, request, slug):
        group = Group.objects.get(slug__iexact=slug)
        bound_form = GroupForm(request.POST, instance=group)

        if bound_form.is_valid():
            new_group = bound_form.save()
            return redirect(new_group)
        return render(request, 'Groups/group_update.html', context = {'form':bound_form, 'group':group})

class StudentUpdate(View):
    def get(self, request, slug):
        if request.user.is_superuser:
            student = Student.objects.get(slug__iexact=slug)
            bound_form = StudentForm(instance=student)
            return render(request, 'Groups/student_update.html', context={'form': bound_form, 'student': student})
        else:
            return render(request, 'Groups/permission_page.html')

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
        if request.user.is_superuser:
            group = Group.objects.get(slug__iexact = slug)
            return render(request, 'Groups/group_delete.html', context = {'group': group})
        else:
            return render(request, 'Groups/permission_page.html')

    def post(self, request, slug):
        group = Group.objects.get(slug__iexact=slug)
        group.delete()
        return redirect('groups_list')

class StudentDelete(View):
    def get(self, request, slug):
        if request.user.is_superuser:
            student = Student.objects.get(slug__iexact = slug)
            return render(request, 'Groups/student_delete.html', context = {'student': student})
        else:
            return render(request, 'Groups/permission_page.html')

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
            count = student.marks.all().count()
            avg = student.avg_mark
            student.avg_mark = (avg*count+new_mark.mark)/(count+1)
            student.marks.add(new_mark)
            student.save()
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
            student = Student.objects.get(slug=slug)
            prev_mark = Mark.objects.get(id=id).mark
            new_mark = bound_form.save()
            count = student.marks.all().count()
            student.avg_mark += (new_mark.mark - prev_mark)/count
            student.save()
            return redirect('marks_list', slug)
        return render(request, 'Groups/mark_update.html', context={'form': bound_form, 'slug': slug, 'id': id})

class MarkDelete(View):
    def get(self, request, slug, id):
        mark = Mark.objects.get(id__iexact=id)
        return render(request, 'Groups/mark_delete.html', context={'mark': mark, 'slug': slug, 'id': id})

    def post(self, request, slug, id):
        student = Student.objects.get(slug=slug)
        mark = Mark.objects.get(id__iexact=id)
        count = student.marks.all().count()
        try:
            student.avg_mark = (count*student.avg_mark-mark.mark)/(count-1)
            student.save()
        except:
            student.avg_mark = 0
        mark.delete()
        return redirect('marks_list', slug)


###
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




