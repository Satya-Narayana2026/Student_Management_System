from django.urls import path

from . import views


app_name = "subjects"


urlpatterns = [

    # Subject List
    path(
        "",
        views.subject_list,
        name="subject_list"
    ),

    # Add Subject
    path(
        "add/",
        views.subject_add,
        name="subject_add"
    ),

    # Edit Subject
    path(
        "edit/<int:pk>/",
        views.subject_edit,
        name="subject_edit"
    ),

    # Delete Subject
    path(
        "delete/<int:pk>/",
        views.subject_delete,
        name="subject_delete"
    ),

    path(
    "courses-by-department/",
    views.courses_by_department,
    name="courses_by_department"
),

]