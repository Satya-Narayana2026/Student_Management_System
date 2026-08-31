from django.urls import path

from . import views


app_name = "results"


urlpatterns = [

    # Result List
    path(
        "",
        views.result_list,
        name="result_list"
    ),

    # Add Result
    path(
        "add/",
        views.result_add,
        name="result_add"
    ),

    # Edit Result
    path(
        "<int:pk>/edit/",
        views.result_edit,
        name="result_edit"
    ),

    # Delete Result
    path(
        "<int:pk>/delete/",
        views.result_delete,
        name="result_delete"
    ),

]