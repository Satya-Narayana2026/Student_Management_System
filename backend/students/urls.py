from django.urls import path

from . import views


app_name = 'students'


urlpatterns = [

    # =========================
    # ADMIN + TEACHER STUDENT MANAGEMENT
    # =========================

    path(
        '',
        views.student_list,
        name='student_list'
    ),

    path(
        'add/',
        views.student_add,
        name='student_add'
    ),

    path(
        '<int:pk>/',
        views.student_detail,
        name='student_detail'
    ),

    path(
        '<int:pk>/edit/',
        views.student_edit,
        name='student_edit'
    ),

    path(
        '<int:pk>/delete/',
        views.student_delete,
        name='student_delete'
    ),


    # =========================
    # STUDENT PERSONAL PAGES
    # =========================

    path(
        'my-profile/',
        views.my_profile,
        name='my_profile'
    ),

    path(
        'my-course/',
        views.my_course,
        name='my_course'
    ),

    path(
    "courses-by-department/",
    views.courses_by_department,
    name="courses_by_department"
),

]