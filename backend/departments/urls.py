from django.urls import path

from . import views


app_name = "departments"


urlpatterns = [

    path(
        "",
        views.department_list,
        name="department_list"
    ),

    path(
        "add/",
        views.department_add,
        name="department_add"
    ),

    path(
        "edit/<int:pk>/",
        views.department_edit,
        name="department_edit"
    ),

    path(
        "delete/<int:pk>/",
        views.department_delete,
        name="department_delete"
    ),

]