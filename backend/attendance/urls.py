from django.urls import path

from . import views


app_name = 'attendance'


urlpatterns = [

    path(
        '',
        views.attendance_list,
        name='attendance_list'
    ),

    path(
        'add/',
        views.attendance_add,
        name='attendance_add'
    ),

    path(
        '<int:pk>/edit/',
        views.attendance_edit,
        name='attendance_edit'
    ),

    path(
        '<int:pk>/delete/',
        views.attendance_delete,
        name='attendance_delete'
    ),

]