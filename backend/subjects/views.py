from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render
)

from .forms import SubjectForm
from .models import Subject

from courses.models import Course
from departments.models import Department
from django.http import JsonResponse


@login_required
def subject_list(request):

    search = request.GET.get(
        "search",
        ""
    )

    department_id = request.GET.get(
        "department",
        ""
    )

    course_id = request.GET.get(
        "course",
        ""
    )

    subjects = Subject.objects.select_related(
        "course",
        "course__department"
    ).order_by(
        "course__department__code",
        "course__code",
        "semester",
        "code"
    )

    if search:

        subjects = subjects.filter(
            Q(name__icontains=search) |
            Q(code__icontains=search) |
            Q(course__name__icontains=search) |
            Q(course__code__icontains=search)
        )

    if department_id:

        subjects = subjects.filter(
            course__department_id=department_id
        )

    if course_id:

        subjects = subjects.filter(
            course_id=course_id
        )

    paginator = Paginator(
        subjects,
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

    courses = Course.objects.select_related(
        "department"
    ).order_by(
        "code"
    )

    return render(
        request,
        "subjects/subject_list.html",
        {
            "page_obj": page_obj,
            "departments": departments,
            "courses": courses,
            "search": search,
            "selected_department": department_id,
            "selected_course": course_id,
        }
    )


@login_required
def subject_add(request):

    if request.method == "POST":

        form = SubjectForm(
            request.POST
        )

        if form.is_valid():

            subject = form.save()

            messages.success(
                request,
                f"Subject {subject.code} added successfully."
            )

            return redirect(
                "subjects:subject_list"
            )

    else:

        form = SubjectForm()

    return render(
        request,
        "subjects/subject_form.html",
        {
            "form": form,
            "title": "Add Subject",
            "button_text": "Save Subject",
        }
    )


@login_required
def subject_edit(request, pk):

    subject = get_object_or_404(
        Subject,
        pk=pk
    )

    if request.method == "POST":

        form = SubjectForm(
            request.POST,
            instance=subject
        )

        if form.is_valid():

            subject = form.save()

            messages.success(
                request,
                f"Subject {subject.code} updated successfully."
            )

            return redirect(
                "subjects:subject_list"
            )

    else:

        form = SubjectForm(
            instance=subject
        )

    return render(
        request,
        "subjects/subject_form.html",
        {
            "form": form,
            "title": "Edit Subject",
            "button_text": "Update Subject",
        }
    )


@login_required
def subject_delete(request, pk):

    subject = get_object_or_404(
        Subject,
        pk=pk
    )

    if request.method == "POST":

        subject_code = subject.code

        subject.delete()

        messages.success(
            request,
            f"Subject {subject_code} deleted successfully."
        )

        return redirect(
            "subjects:subject_list"
        )

    return render(
        request,
        "subjects/subject_confirm_delete.html",
        {
            "subject": subject
        }
    )

@login_required
def courses_by_department(request):

    department_id = request.GET.get("department_id")

    if not department_id:
        return JsonResponse(
            {
                "courses": []
            }
        )

    courses = Course.objects.filter(
        department_id=department_id
    ).order_by("code")

    data = []

    for course in courses:

        data.append(
            {
                "id": course.id,
                "name": course.name,
                "code": course.code,
            }
        )

    return JsonResponse(
        {
            "courses": data
        }
    )