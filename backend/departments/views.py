from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models.deletion import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render

from .forms import DepartmentForm
from .models import Department


def is_admin(user):
    return user.is_superuser


# =========================
# DEPARTMENT LIST
# =========================

@login_required
def department_list(request):

    if not is_admin(request.user):
        messages.error(
            request,
            "You do not have permission to manage departments."
        )
        return redirect("dashboard:dashboard")

    search = request.GET.get("search", "")

    departments = Department.objects.all().order_by("code")

    if search:

        departments = departments.filter(
            Q(name__icontains=search) |
            Q(code__icontains=search)
        )

    paginator = Paginator(
        departments,
        10
    )

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(
        page_number
    )

    return render(
        request,
        "departments/department_list.html",
        {
            "page_obj": page_obj,
            "search": search,
        }
    )


# =========================
# ADD DEPARTMENT
# =========================

@login_required
def department_add(request):

    if not is_admin(request.user):
        messages.error(
            request,
            "You do not have permission to add departments."
        )
        return redirect("dashboard:dashboard")

    if request.method == "POST":

        form = DepartmentForm(
            request.POST
        )

        if form.is_valid():

            department = form.save()

            messages.success(
                request,
                f"Department {department.code} added successfully."
            )

            return redirect(
                "departments:department_list"
            )

    else:

        form = DepartmentForm()

    return render(
        request,
        "departments/department_form.html",
        {
            "form": form,
            "title": "Add Department",
            "button_text": "Save Department",
        }
    )


# =========================
# EDIT DEPARTMENT
# =========================

@login_required
def department_edit(request, pk):

    if not is_admin(request.user):
        messages.error(
            request,
            "You do not have permission to edit departments."
        )
        return redirect("dashboard:dashboard")

    department = get_object_or_404(
        Department,
        pk=pk
    )

    if request.method == "POST":

        form = DepartmentForm(
            request.POST,
            instance=department
        )

        if form.is_valid():

            department = form.save()

            messages.success(
                request,
                f"Department {department.code} updated successfully."
            )

            return redirect(
                "departments:department_list"
            )

    else:

        form = DepartmentForm(
            instance=department
        )

    return render(
        request,
        "departments/department_form.html",
        {
            "form": form,
            "title": "Edit Department",
            "button_text": "Update Department",
        }
    )


# =========================
# DELETE DEPARTMENT
# =========================

@login_required
def department_delete(request, pk):

    if not is_admin(request.user):
        messages.error(
            request,
            "You do not have permission to delete departments."
        )
        return redirect("dashboard:dashboard")

    department = get_object_or_404(
        Department,
        pk=pk
    )

    if request.method == "POST":

        department_code = department.code

        try:

            department.delete()

            messages.success(
                request,
                f"Department {department_code} deleted successfully."
            )

        except ProtectedError:

            messages.error(
                request,
                f"Department {department_code} cannot be deleted "
                f"because courses are assigned to this department."
            )

        return redirect(
            "departments:department_list"
        )

    return render(
        request,
        "departments/department_confirm_delete.html",
        {
            "department": department
        }
    )