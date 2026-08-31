from django.urls import path

from . import views


app_name = "courses"


urlpatterns = [

    path(
        "",
        views.course_list,
        name="course_list"
    ),

    path(
        "add/",
        views.course_add,
        name="course_add"
    ),

    path(
        "edit/<int:pk>/",
        views.course_edit,
        name="course_edit"
    ),

    path(
        "delete/<int:pk>/",
        views.course_delete,
        name="course_delete"
    ),

]