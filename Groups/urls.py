from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import SimpleRouter

from . import views
from .views import *

urlpatterns = [
    path('', views.home_page, name='home_page'),

    path('any', views.any),

    path('stat/<str:slug>', views.stat, name='stat_url'),

    path('api/students', views.StudentsView.as_view()),
    path('api/student/<str:id>', views.SingleStudentView.as_view()),
    path('api/groups', views.GroupsView.as_view()),
    path('api/group/<str:id>', views.SingleGroupView.as_view()),
    path('api/subjects', views.SubjectsView.as_view()),
    path('api/subject/<str:id>', views.SingleSubjectView.as_view()),


    path('groups', views.GroupsList.as_view(), name='groups_list'),
    path('students', views.StudentsList.as_view(), name='students_list'),
    path('student/create/', StudentCreate.as_view(), name='student_create'),
    path('student/<str:slug>/', StudentDetail.as_view(), name='student_detail'),
    path('student/<str:slug>/delete', StudentDelete.as_view(), name='student_delete'),
    path('student/<str:slug>/update', StudentUpdate.as_view(), name='student_update'),

    path('student/<str:slug>/marks', views.MarkList.as_view(), name='marks_list'),
    path('student/<str:slug>/marks/create', views.MarkCreate.as_view(), name='mark_create'),

    path('student/<str:slug>/marks/<int:id>/update', views.MarkUpdate.as_view(), name='mark_update'),
    path('student/<str:slug>/marks/<int:id>/delete', views.MarkDelete.as_view(), name='mark_delete'),

    path('group/create/', GroupCreate.as_view(), name='group_create'),
    path('group/<str:slug>/', GroupDetail.as_view(), name='group_detail'),
    path('group/<str:slug>/stats', GroupStats.as_view(), name='group_stats'),
    path('group/<str:slug>/update/', GroupUpdate.as_view(), name='group_update'),
    path('group/<str:slug>/delete/', GroupDelete.as_view(), name='group_delete'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

