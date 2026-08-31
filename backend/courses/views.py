from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models.deletion import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CourseForm
from .models import Course
from departments.models import Department


# =========================
# COURSE LIST
# =========================

@login_required
def course_list(request):

    search = request.GET.get(
        "search",
        ""
    )

    department_id = request.GET.get(
        "department",
        ""
    )

    courses = Course.objects.select_related(
        "department"
    ).order_by(
        "department__code",
        "code"
    )

    # SEARCH
    if search:

        courses = courses.filter(
            Q(name__icontains=search) |
            Q(code__icontains=search) |
            Q(department__name__icontains=search) |
            Q(department__code__icontains=search)
        )

    # DEPARTMENT FILTER
    if department_id:

        courses = courses.filter(
            department_id=department_id
        )

    paginator = Paginator(
        courses,
        10
    )

    page_number = request.GET.get(
        "page"
    )

    page_obj = paginator.get_page(
        page_number
    )

    departments = Department.objects.all().order_by(
        "code"
    )

    return render(
        request,
        "courses/course_list.html",
        {
            "page_obj": page_obj,
            "departments": departments,
            "search": search,
            "selected_department": department_id,
        }
    )


# =========================
# ADD COURSE
# =========================

@login_required
def course_add(request):

    if request.method == "POST":

        form = CourseForm(
            request.POST
        )

        if form.is_valid():

            course = form.save()

            messages.success(
                request,
                f"Course {course.code} added successfully."
            )

            return redirect(
                "courses:course_list"
            )

    else:

        form = CourseForm()

    return render(
        request,
        "courses/course_form.html",
        {
            "form": form,
            "title": "Add Course",
            "button_text": "Save Course",
        }
    )


# =========================
# EDIT COURSE
# =========================

@login_required
def course_edit(request, pk):

    course = get_object_or_404(
        Course,
        pk=pk
    )

    if request.method == "POST":

        form = CourseForm(
            request.POST,
            instance=course
        )

        if form.is_valid():

            course = form.save()

            messages.success(
                request,
                f"Course {course.code} updated successfully."
            )

            return redirect(
                "courses:course_list"
            )

    else:

        form = CourseForm(
            instance=course
        )

    return render(
        request,
        "courses/course_form.html",
        {
            "form": form,
            "title": "Edit Course",
            "button_text": "Update Course",
        }
    )


# =========================
# DELETE COURSE
# =========================

@login_required
def course_delete(request, pk):

    course = get_object_or_404(
        Course,
        pk=pk
    )

    if request.method == "POST":

        course_code = course.code

        try:

            course.delete()

            messages.success(
                request,
                f"Course {course_code} deleted successfully."
            )

        except ProtectedError:

            messages.error(
                request,
                f"Course {course_code} cannot be deleted because "
                f"students are currently assigned to this course."
            )

        return redirect(
            "courses:course_list"
        )

    return render(
        request,
        "courses/course_confirm_delete.html",
        {
            "course": course
        }
    )