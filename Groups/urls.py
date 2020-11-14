from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.home_page, name='home_page'),

    path('signup', views.signup, name='signup_url'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})',
         views.activate, name='activate'),
    path('signin', views.signin, name='signin_url'),
    path('signout', views.signout, name='signout_url'),
    path('profile', views.profile, name='profile'),
    path('toDoList', views.toDoList, name='toDoList'),
    path('add_profile/', views.profile_add, name='profile_add'),

    path('api/students', views.StudentsView.as_view()),
    path('api/student/<str:id>', views.SingleStudentView.as_view()),
    path('api/groups', views.GroupsView.as_view()),
    path('api/group/<str:id>', views.SingleGroupView.as_view()),
    path('api/subjects', views.SubjectsView.as_view()),
    path('api/subject/<str:id>', views.SingleSubjectView.as_view()),

    path('rating', views.best_gpa, name='rating'),
    path('groups', login_required(views.GroupsList.as_view()), name='groups_list'),
    path('students', login_required(views.StudentsList.as_view()), name='students_list'),
    path('student/create/', login_required(StudentCreate.as_view()), name='student_create'),
    path('student/<str:slug>/', login_required(StudentDetail.as_view()), name='student_detail'),
    path('student/<str:slug>/delete', login_required(StudentDelete.as_view()), name='student_delete'),
    path('student/<str:slug>/update', login_required(StudentUpdate.as_view()), name='student_update'),

    path('student/<str:slug>/marks', login_required(views.MarkList.as_view()), name='marks_list'),
    path('student/<str:slug>/marks/create', login_required(views.MarkCreate.as_view()), name='mark_create'),

    path('student/<str:slug>/marks/<int:id>/update', login_required(views.MarkUpdate.as_view()), name='mark_update'),
    path('student/<str:slug>/marks/<int:id>/delete', login_required(views.MarkDelete.as_view()), name='mark_delete'),

    path('group/create/', login_required(GroupCreate.as_view()), name='group_create'),
    path('group/<str:slug>/', login_required(GroupDetail.as_view()), name='group_detail'),
    path('group/<str:slug>/map', login_required(GroupMap.as_view()), name='group_map'),
    path('group/<str:slug>/update/', login_required(GroupUpdate.as_view()), name='group_update'),
    path('group/<str:slug>/delete/', login_required(GroupDelete.as_view()), name='group_delete'),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
