from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)
from django.db.models import Q

from .models import Attendance
from .forms import AttendanceForm


# =========================
# HELPER FUNCTIONS
# =========================

def is_admin(user):

    return (
        user.is_superuser
        or user.groups.filter(
            name='Admin'
        ).exists()
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
# ATTENDANCE LIST
#
# Admin   -> View all
# Teacher -> View all
# Student -> View only own
# =========================

@login_required
def attendance_list(request):

    search = request.GET.get(
        'search',
        ''
    )

    selected_date = request.GET.get(
        'date',
        ''
    )


    # =========================
    # ADMIN + TEACHER
    # =========================

    if is_admin(request.user) or is_teacher(request.user):

        attendance_records = Attendance.objects.select_related(
            'student',
            'student__course'
        ).all().order_by(
            '-date'
        )


        # SEARCH
        if search:

            attendance_records = attendance_records.filter(

                Q(
                    student__student_id__icontains=search
                )
                |
                Q(
                    student__first_name__icontains=search
                )
                |
                Q(
                    student__last_name__icontains=search
                )

            )


        # DATE FILTER
        if selected_date:

            attendance_records = attendance_records.filter(
                date=selected_date
            )


        return render(
            request,
            'attendance/attendance_list.html',
            {
                'attendance_records': attendance_records,

                'search': search,

                'selected_date': selected_date,

                'can_manage_attendance': True,

                'is_admin': is_admin(
                    request.user
                ),
            }
        )


    # =========================
    # STUDENT
    #
    # ONLY OWN ATTENDANCE
    # =========================

    if is_student(request.user):

        attendance_records = Attendance.objects.select_related(
            'student',
            'student__course'
        ).filter(
            student__user=request.user
        ).order_by(
            '-date'
        )


        # DATE FILTER ONLY
        if selected_date:

            attendance_records = attendance_records.filter(
                date=selected_date
            )


        return render(
            request,
            'attendance/attendance_list.html',
            {
                'attendance_records': attendance_records,

                'search': '',

                'selected_date': selected_date,

                # Student cannot add/edit/delete
                'can_manage_attendance': False,

                'is_admin': False,
            }
        )


    # =========================
    # NO PERMISSION
    # =========================

    messages.error(
        request,
        'You do not have permission to view attendance.'
    )

    return redirect(
        'dashboard:dashboard'
    )


# =========================
# ADD ATTENDANCE
#
# ADMIN + TEACHER ONLY
# =========================

@login_required
def attendance_add(request):

    if not is_admin(
        request.user
    ) and not is_teacher(
        request.user
    ):

        messages.error(
            request,
            'You do not have permission to add attendance.'
        )

        return redirect(
            'attendance:attendance_list'
        )


    if request.method == 'POST':

        form = AttendanceForm(
            request.POST
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Attendance added successfully.'
            )

            return redirect(
                'attendance:attendance_list'
            )

    else:

        form = AttendanceForm()


    return render(
        request,
        'attendance/attendance_form.html',
        {
            'form': form,
            'title': 'Add Attendance',
            'button_text': 'Save Attendance',
        }
    )


# =========================
# EDIT ATTENDANCE
#
# ADMIN + TEACHER ONLY
# =========================

@login_required
def attendance_edit(request, pk):

    if not is_admin(
        request.user
    ) and not is_teacher(
        request.user
    ):

        messages.error(
            request,
            'You do not have permission to edit attendance.'
        )

        return redirect(
            'attendance:attendance_list'
        )


    attendance = get_object_or_404(
        Attendance,
        pk=pk
    )


    if request.method == 'POST':

        form = AttendanceForm(
            request.POST,
            instance=attendance
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Attendance updated successfully.'
            )

            return redirect(
                'attendance:attendance_list'
            )

    else:

        form = AttendanceForm(
            instance=attendance
        )


    return render(
        request,
        'attendance/attendance_form.html',
        {
            'form': form,
            'title': 'Edit Attendance',
            'button_text': 'Update Attendance',
        }
    )


# =========================
# DELETE ATTENDANCE
#
# ADMIN ONLY
# =========================

@login_required
def attendance_delete(request, pk):

    if not is_admin(
        request.user
    ):

        messages.error(
            request,
            'Only Admin can delete attendance.'
        )

        return redirect(
            'attendance:attendance_list'
        )


    attendance = get_object_or_404(
        Attendance,
        pk=pk
    )


    if request.method == 'POST':

        attendance.delete()

        messages.success(
            request,
            'Attendance deleted successfully.'
        )

        return redirect(
            'attendance:attendance_list'
        )


    return render(
        request,
        'attendance/attendance_confirm_delete.html',
        {
            'attendance': attendance
        }
    )