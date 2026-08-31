from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from students.models import Student
from teachers.models import Teacher
from courses.models import Course
from subjects.models import Subject
from attendance.models import Attendance
from results.models import Result


@login_required(login_url='accounts:login')
def dashboard(request):

    # =========================
    # STUDENT DASHBOARD
    # =========================

    if request.user.groups.filter(
        name='Student'
    ).exists():

        return render(
            request,
            'dashboard/student_dashboard.html'
        )


    # =========================
    # TEACHER DASHBOARD
    # =========================

    if request.user.groups.filter(
        name='Teacher'
    ).exists():

        total_students = Student.objects.count()

        total_courses = Course.objects.count()

        total_attendance = Attendance.objects.count()

        total_results = Result.objects.count()

        return render(
            request,
            'dashboard/teacher_dashboard.html',
            {
                'total_students': total_students,
                'total_courses': total_courses,
                'total_attendance': total_attendance,
                'total_results': total_results,
            }
        )


    # =========================
    # ADMIN DASHBOARD
    # =========================

    total_students = Student.objects.count()

    total_teachers = Teacher.objects.count()

    total_courses = Course.objects.count()

    total_subjects = Subject.objects.count()

    total_attendance = Attendance.objects.count()

    total_results = Result.objects.count()

    return render(
        request,
        'dashboard/admin_dashboard.html',
        {
            'total_students': total_students,
            'total_teachers': total_teachers,
            'total_courses': total_courses,
            'total_subjects': total_subjects,
            'total_attendance': total_attendance,
            'total_results': total_results,
        }
    )