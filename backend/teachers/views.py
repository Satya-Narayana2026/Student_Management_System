from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib.auth.models import (
    User,
    Group
)

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db import transaction
from django.db.models import Q

from .models import Teacher
from .forms import TeacherForm

from departments.models import Department
from subjects.models import Subject


# =========================
# TEACHER LIST
# =========================

@login_required
def teacher_list(request):

    search = request.GET.get(
        "search",
        ""
    )

    department_id = request.GET.get(
        "department",
        ""
    )

    teachers = Teacher.objects.select_related(
        "department"
    ).prefetch_related(
        "subjects"
    ).all().order_by(
        "department__code",
        "-created_at"
    )

    if search:

        teachers = teachers.filter(

            Q(teacher_id__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(email__icontains=search) |
            Q(designation__icontains=search) |
            Q(department__name__icontains=search) |
            Q(department__code__icontains=search)

        )

    if department_id:

        teachers = teachers.filter(
            department_id=department_id
        )

    departments = Department.objects.all().order_by(
        "code"
    )

    return render(
        request,
        "teachers/teacher_list.html",
        {
            "teachers": teachers,
            "departments": departments,
            "search": search,
            "selected_department": department_id,
        }
    )


# =========================
# SUBJECTS BY DEPARTMENT
# =========================

@login_required
def subjects_by_department(request):

    department_id = request.GET.get(
        "department_id"
    )

    if not department_id:

        return JsonResponse({
            "subjects": []
        })

    subjects = Subject.objects.filter(
        course__department_id=department_id
    ).select_related(
        "course"
    ).order_by(
        "course__code",
        "semester",
        "code"
    )

    data = []

    for subject in subjects:

        data.append({

            "id": subject.id,

            "code": subject.code,

            "name": subject.name,

            "semester": subject.semester,

            "course": subject.course.code,

        })

    return JsonResponse({
        "subjects": data
    })


# =========================
# ADD TEACHER
# =========================

@login_required
def teacher_add(request):

    if request.method == "POST":

        form = TeacherForm(
            request.POST
        )

        if form.is_valid():

            username = form.cleaned_data[
                "username"
            ]

            password = form.cleaned_data[
                "password"
            ]

            with transaction.atomic():

                # Create Django login user

                user = User.objects.create_user(
                    username=username,
                    password=password,
                    first_name=form.cleaned_data[
                        "first_name"
                    ],
                    last_name=form.cleaned_data[
                        "last_name"
                    ],
                    email=form.cleaned_data[
                        "email"
                    ]
                )

                # Teacher group

                teacher_group, created = (
                    Group.objects.get_or_create(
                        name="Teacher"
                    )
                )

                user.groups.add(
                    teacher_group
                )

                # Create teacher profile

                teacher = form.save(
                    commit=False
                )

                teacher.user = user

                teacher.save()

                # IMPORTANT:
                # Save Many-to-Many subjects

                form.save_m2m()

            messages.success(
                request,
                f"Teacher {teacher.first_name} "
                f"{teacher.last_name} created successfully."
            )

            return redirect(
                "teachers:teacher_list"
            )

    else:

        form = TeacherForm()

    return render(
        request,
        "teachers/teacher_form.html",
        {
            "form": form,
            "title": "Add Teacher",
            "button_text": "Save Teacher",
        }
    )


# =========================
# EDIT TEACHER
# =========================

@login_required
def teacher_edit(request, pk):

    teacher = get_object_or_404(
        Teacher,
        pk=pk
    )

    if request.method == "POST":

        form = TeacherForm(
            request.POST,
            instance=teacher
        )

        if form.is_valid():

            teacher = form.save()

            # Update connected User

            if teacher.user:

                teacher.user.first_name = (
                    teacher.first_name
                )

                teacher.user.last_name = (
                    teacher.last_name
                )

                teacher.user.email = (
                    teacher.email
                )

                teacher.user.save()

            messages.success(
                request,
                "Teacher updated successfully."
            )

            return redirect(
                "teachers:teacher_list"
            )

    else:

        initial_data = {}

        if teacher.user:

            initial_data["username"] = (
                teacher.user.username
            )

        form = TeacherForm(
            instance=teacher,
            initial=initial_data
        )

    return render(
        request,
        "teachers/teacher_form.html",
        {
            "form": form,
            "title": "Edit Teacher",
            "button_text": "Update Teacher",
        }
    )


# =========================
# DELETE TEACHER
# =========================

@login_required
def teacher_delete(request, pk):

    teacher = get_object_or_404(
        Teacher,
        pk=pk
    )

    if request.method == "POST":

        user = teacher.user

        teacher_name = (
            f"{teacher.first_name} "
            f"{teacher.last_name}"
        )

        teacher.delete()

        if user:

            user.delete()

        messages.success(
            request,
            f"Teacher {teacher_name} deleted successfully."
        )

        return redirect(
            "teachers:teacher_list"
        )

    return render(
        request,
        "teachers/teacher_confirm_delete.html",
        {
            "teacher": teacher
        }
    )


# =========================
# TEACHER MY PROFILE
# =========================

@login_required
def my_profile(request):

    teacher = get_object_or_404(
        Teacher.objects.select_related(
            "department"
        ),
        user=request.user
    )

    return render(
        request,
        "teachers/my_profile.html",
        {
            "teacher": teacher
        }
    )


# =========================
# TEACHER MY SUBJECTS
# =========================

@login_required
def my_subjects(request):

    teacher = get_object_or_404(
        Teacher.objects.select_related(
            "department"
        ).prefetch_related(
            "subjects__course"
        ),
        user=request.user
    )

    subjects = teacher.subjects.all().order_by(
        "course__code",
        "semester",
        "code"
    )

    return render(
        request,
        "teachers/my_subjects.html",
        {
            "teacher": teacher,
            "subjects": subjects
        }
    )