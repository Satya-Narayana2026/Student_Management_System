from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Result
from .forms import ResultForm


# ==========================================
# RESULT LIST
# ==========================================

@login_required
def result_list(request):

    user = request.user

    # Check user role
    is_admin = user.is_superuser
    is_teacher = user.groups.filter(name="Teacher").exists()
    is_student = user.groups.filter(name="Student").exists()

    # ==========================================
    # ADMIN AND TEACHER
    # ==========================================

    if is_admin or is_teacher:

        results = Result.objects.all().order_by("-id")

    # ==========================================
    # STUDENT
    # ==========================================

    elif is_student:

        try:

            student = user.student_profile

            results = Result.objects.filter(
                student=student
            ).order_by("-id")

        except:

            results = Result.objects.none()

    # ==========================================
    # OTHER USERS
    # ==========================================

    else:

        results = Result.objects.none()

    context = {

        "results": results,

        "is_admin": is_admin,

        "is_teacher": is_teacher,

        "is_student": is_student,

        "can_manage_results": (
            is_admin or is_teacher
        ),

    }

    return render(
        request,
        "results/result_list.html",
        context
    )


# ==========================================
# ADD RESULT
# ADMIN AND TEACHER ONLY
# ==========================================

@login_required
def result_add(request):

    user = request.user

    is_admin = user.is_superuser
    is_teacher = user.groups.filter(
        name="Teacher"
    ).exists()

    # Students cannot add results
    if not (is_admin or is_teacher):

        messages.error(
            request,
            "You do not have permission to add results."
        )

        return redirect(
            "results:result_list"
        )

    if request.method == "POST":

        form = ResultForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Result added successfully."
            )

            return redirect(
                "results:result_list"
            )

    else:

        form = ResultForm()

    return render(
        request,
        "results/result_form.html",
        {
            "form": form,
            "title": "Add Result"
        }
    )


# ==========================================
# EDIT RESULT
# ADMIN AND TEACHER ONLY
# ==========================================

@login_required
def result_edit(request, pk):

    user = request.user

    is_admin = user.is_superuser
    is_teacher = user.groups.filter(
        name="Teacher"
    ).exists()

    # Students cannot edit results
    if not (is_admin or is_teacher):

        messages.error(
            request,
            "You do not have permission to edit results."
        )

        return redirect(
            "results:result_list"
        )

    result = get_object_or_404(
        Result,
        pk=pk
    )

    if request.method == "POST":

        form = ResultForm(
            request.POST,
            instance=result
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Result updated successfully."
            )

            return redirect(
                "results:result_list"
            )

    else:

        form = ResultForm(
            instance=result
        )

    return render(
        request,
        "results/result_form.html",
        {
            "form": form,
            "title": "Edit Result"
        }
    )


# ==========================================
# DELETE RESULT
# ADMIN ONLY
# ==========================================

@login_required
def result_delete(request, pk):

    user = request.user

    # Only admin can delete
    if not user.is_superuser:

        messages.error(
            request,
            "Only administrators can delete results."
        )

        return redirect(
            "results:result_list"
        )

    result = get_object_or_404(
        Result,
        pk=pk
    )

    if request.method == "POST":

        result.delete()

        messages.success(
            request,
            "Result deleted successfully."
        )

        return redirect(
            "results:result_list"
        )

    return render(
        request,
        "results/result_confirm_delete.html",
        {
            "result": result
        }
    )