from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from rest_framework.routers import SimpleRouter

from . import views
from .views import *


router = SimpleRouter()
router.register('api/group', GroupView)
router.register('api/student', StudentView)

urlpatterns = [
    path('api/groups', views.groups_api, name='api_groups_list'),
    path('', views.home_page, name='home_page'),
    path('groups', views.groups_list, name='groups_list'),
    path('students', views.students_list, name='students_list'),
    path('student/create/', StudentCreate.as_view(), name='student_create'),
    path('student/<str:slug>/', StudentDetail.as_view(), name='student_detail'),
    path('student/<str:slug>/delete', StudentDelete.as_view(), name='student_delete'),
    path('student/<str:slug>/update', StudentUpdate.as_view(), name='student_update'),
    path('group/create/', GroupCreate.as_view(), name='group_create'),
    path('group/<str:slug>/', GroupDetail.as_view(), name='group_detail'),
    path('group/<str:slug>/update/', GroupUpdate.as_view(), name='group_update'),
    path('group/<str:slug>/delete/', GroupDelete.as_view(), name='group_delete'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += router.urls
