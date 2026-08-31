from django.urls import path

from . import views


app_name = 'teachers'


urlpatterns = [
    path('', views.teacher_list, name='teacher_list'),
    path('add/', views.teacher_add, name='teacher_add'),
    path('edit/<int:pk>/', views.teacher_edit, name='teacher_edit'),
    path('delete/<int:pk>/', views.teacher_delete, name='teacher_delete'),
    path(
    "subjects-by-department/",
    views.subjects_by_department,
    name="subjects_by_department"
  ),

  path(
    "my-profile/",
    views.my_profile,
    name="my_profile"
),

path(
    "my-subjects/",
    views.my_subjects,
    name="my_subjects"
),
]