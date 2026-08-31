from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import StudentForm
from .models import Student

from departments.models import Department
from courses.models import Course
from django.http import JsonResponse

# =========================
# HELPER FUNCTIONS
# =========================

def is_admin(user):

    return (
        user.is_superuser
        or user.groups.filter(name='Admin').exists()
    )


def is_teacher(user):

    return user.groups.filter(
        name='Teacher'
    ).exists()


def is_student(user):

    return user.groups.filter(
        name='Student'
    ).exists()


# =========================
# STUDENT LIST
# ADMIN + TEACHER
# =========================

@login_required
def student_list(request):

    # Only Admin and Teacher can view all students
    if not is_admin(request.user) and not is_teacher(request.user):

        messages.error(
            request,
            'You do not have permission to view all students.'
        )

        return redirect(
            'dashboard:dashboard'
        )

    search = request.GET.get(
        'search',
        ''
    )

    department_id = request.GET.get(
        'department',
        ''
    )

    course_id = request.GET.get(
        'course',
        ''
    )

    # =========================
    # STUDENT QUERYSET
    # =========================

    students = Student.objects.select_related(
        'course',
        'course__department'
    ).order_by(
        'course__department__code',
        'course__code',
        'student_id'
    )

    # =========================
    # SEARCH
    # =========================

    if search:

        students = students.filter(

            Q(student_id__icontains=search) |

            Q(first_name__icontains=search) |

            Q(last_name__icontains=search) |

            Q(email__icontains=search) |

            Q(phone__icontains=search) |

            Q(course__name__icontains=search) |

            Q(course__code__icontains=search) |

            Q(course__department__name__icontains=search) |

            Q(course__department__code__icontains=search)

        )

    # =========================
    # DEPARTMENT FILTER
    # =========================

    if department_id:

        students = students.filter(
            course__department_id=department_id
        )

    # =========================
    # COURSE FILTER
    # =========================

    if course_id:

        students = students.filter(
            course_id=course_id
        )

    # =========================
    # PAGINATION
    # =========================

    paginator = Paginator(
        students,
        10
    )

    page_number = request.GET.get(
        'page'
    )

    page_obj = paginator.get_page(
        page_number
    )

    # =========================
    # FILTER DATA
    # =========================

    from departments.models import Department
    from courses.models import Course

    departments = Department.objects.all().order_by(
        'code'
    )

    courses = Course.objects.select_related(
        'department'
    ).all().order_by(
        'code'
    )

    # =========================
    # PERMISSIONS
    # =========================

    can_manage_students = is_admin(
        request.user
    )

    # =========================
    # RENDER
    # =========================

    return render(
        request,
        'students/list.html',
        {
            'page_obj': page_obj,
            'search': search,
            'departments': departments,
            'courses': courses,
            'selected_department': department_id,
            'selected_course': course_id,
            'can_manage_students': can_manage_students,
        }
    )


# =========================
# STUDENT DETAIL
# ADMIN + TEACHER + OWN STUDENT
# =========================

@login_required
def student_detail(request, pk):

    student = get_object_or_404(
        Student.objects.select_related(
            'course'
        ),
        pk=pk
    )

    # Admin and Teacher can view any student
    if is_admin(request.user) or is_teacher(request.user):

        return render(
            request,
            'students/detail.html',
            {
                'student': student,
            }
        )

    # Student can view only their own profile
    if is_student(request.user):

        if student.user == request.user:

            return render(
                request,
                'students/detail.html',
                {
                    'student': student,
                }
            )

    messages.error(
        request,
        'You do not have permission to view this student.'
    )

    return redirect(
        'dashboard:dashboard'
    )


# =========================
# ADD STUDENT
# ADMIN ONLY
# =========================

@login_required
def student_add(request):

    if not is_admin(request.user):

        messages.error(
            request,
            'Only Admin can add students.'
        )

        return redirect(
            'dashboard:dashboard'
        )

    if request.method == 'POST':

        form = StudentForm(
            request.POST
        )

        if form.is_valid():

            username = form.cleaned_data.get(
                'username'
            )

            password = form.cleaned_data.get(
                'password'
            )

            if not username or not password:

                messages.error(
                    request,
                    'Username and password are required for student login.'
                )

            elif User.objects.filter(
                username=username
            ).exists():

                messages.error(
                    request,
                    'This username already exists.'
                )

            else:

                with transaction.atomic():

                    # Create login user
                    user = User.objects.create_user(
                        username=username,
                        password=password,
                        email=form.cleaned_data[
                            'email'
                        ]
                    )

                    # Add Student group
                    student_group = Group.objects.get(
                        name='Student'
                    )

                    user.groups.add(
                        student_group
                    )

                    # Create Student profile
                    student = form.save(
                        commit=False
                    )

                    student.user = user

                    student.save()

                messages.success(
                    request,
                    f'Student {student.student_id} and '
                    f'login account created successfully.'
                )

                return redirect(
                    'students:student_list'
                )

    else:

        form = StudentForm()

    return render(
        request,
        'students/form.html',
        {
            'form': form,
            'title': 'Add Student',
            'button_text': 'Add Student',
        }
    )


# =========================
# EDIT STUDENT
# ADMIN ONLY
# =========================

@login_required
def student_edit(request, pk):

    if not is_admin(request.user):

        messages.error(
            request,
            'Only Admin can edit student information.'
        )

        return redirect(
            'dashboard:dashboard'
        )

    student = get_object_or_404(
        Student,
        pk=pk
    )

    if request.method == 'POST':

        form = StudentForm(
            request.POST,
            instance=student
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                f'Student {student.student_id} '
                f'updated successfully.'
            )

            return redirect(
                'students:student_list'
            )

    else:

        form = StudentForm(
            instance=student
        )

    return render(
        request,
        'students/form.html',
        {
            'form': form,
            'title': 'Edit Student',
            'button_text': 'Update Student',
        }
    )


# =========================
# DELETE STUDENT
# ADMIN ONLY
# =========================

@login_required
def student_delete(request, pk):

    if not is_admin(request.user):

        messages.error(
            request,
            'Only Admin can delete students.'
        )

        return redirect(
            'dashboard:dashboard'
        )

    student = get_object_or_404(
        Student,
        pk=pk
    )

    if request.method == 'POST':

        student_id = student.student_id

        # Save related user before deleting
        user = student.user

        # Delete student
        student.delete()

        # Delete login account
        if user:

            user.delete()

        messages.success(
            request,
            f'Student {student_id} deleted successfully.'
        )

        return redirect(
            'students:student_list'
        )

    return render(
        request,
        'students/delete.html',
        {
            'student': student,
        }
    )



# =========================
# STUDENT MY PROFILE
# =========================

@login_required
def my_profile(request):

    # Only Student can access
    if not is_student(request.user):

        messages.error(
            request,
            'You do not have permission to view this page.'
        )

        return redirect(
            'dashboard:dashboard'
        )

    student = get_object_or_404(
        Student.objects.select_related('course'),
        user=request.user
    )

    return render(
        request,
        'students/my_profile.html',
        {
            'student': student,
        }
    )


# =========================
# STUDENT MY COURSE
# =========================

@login_required
def my_course(request):

    # Only Student can access
    if not is_student(request.user):

        messages.error(
            request,
            'You do not have permission to view this page.'
        )

        return redirect(
            'dashboard:dashboard'
        )

    student = get_object_or_404(
        Student.objects.select_related('course'),
        user=request.user
    )

    subjects = []

    if student.course:

        subjects = student.course.subjects.all()

    return render(
        request,
        'students/my_course.html',
        {
            'student': student,
            'course': student.course,
            'subjects': subjects,
        }
    )


# =========================
# COURSES BY DEPARTMENT
# =========================

@login_required
def courses_by_department(request):

    department_id = request.GET.get(
        'department_id'
    )

    if not department_id:

        return JsonResponse({
            'courses': []
        })

    courses = Course.objects.filter(
        department_id=department_id
    ).order_by(
        'code'
    )

    data = []

    for course in courses:

        data.append({
            'id': course.id,
            'name': course.name,
            'code': course.code,
        })

    return JsonResponse({
        'courses': data
    })