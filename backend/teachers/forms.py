from django import forms
from django.contrib.auth.models import User

from .models import Teacher
from departments.models import Department
from subjects.models import Subject


class TeacherForm(forms.ModelForm):

    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Create username",
            }
        )
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Create password",
            }
        )
    )

    department = forms.ModelChoiceField(
        queryset=Department.objects.all().order_by("code"),
        required=True,
        empty_label="Select Department",
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "id": "teacher-department",
            }
        ),
    )

    # IMPORTANT:
    # Render subjects as checkboxes.
    subjects = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple(
            attrs={
                "class": "teacher-subject-checkboxes",
            }
        ),
    )

    class Meta:

        model = Teacher

        fields = [
            "teacher_id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "department",
            "subjects",
            "designation",
            "qualification",
            "joining_date",
            "address",
        ]

        widgets = {

            "teacher_id": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter teacher ID",
                }
            ),

            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter first name",
                }
            ),

            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter last name",
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter email address",
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter phone number",
                }
            ),

            "designation": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Example: Assistant Professor",
                }
            ),

            "qualification": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Example: M.Tech, Ph.D",
                }
            ),

            "joining_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "address": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter address",
                    "rows": 4,
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # Department selected in the submitted form
        department_id = self.data.get("department")

        # Existing teacher's department while editing
        if not department_id and self.instance.pk:
            department_id = self.instance.department_id

        if department_id:

            self.fields["subjects"].queryset = (
                Subject.objects
                .filter(
                    course__department_id=department_id
                )
                .select_related("course")
                .order_by(
                    "course__code",
                    "semester",
                    "code"
                )
            )

        else:

            self.fields["subjects"].queryset = (
                Subject.objects.none()
            )

    def clean_username(self):

        username = self.cleaned_data["username"]

        queryset = User.objects.filter(
            username=username
        )

        # When editing, allow the existing username
        if self.instance.pk and self.instance.user:

            queryset = queryset.exclude(
                pk=self.instance.user.pk
            )

        if queryset.exists():

            raise forms.ValidationError(
                "This username already exists."
            )

        return username