from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    # Dashboard
    path("", include("dashboard.urls")),

    # Accounts
    path("accounts/", include("accounts.urls")),

    # Students
    path("students/", include("students.urls")),

    # Teachers
    path("teachers/", include("teachers.urls")),

    # Courses
    path("courses/", include("courses.urls")),

    # Subjects
    path(
    "subjects/",
    include("subjects.urls")
    ),

    # Attendance
    path("attendance/", include("attendance.urls")),

    # Results
    path("results/", include("results.urls")),

    path(
    "departments/",
    include("departments.urls")
    ),
]