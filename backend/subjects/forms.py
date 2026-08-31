from django import forms

from .models import Subject
from courses.models import Course
from departments.models import Department


class SubjectForm(forms.ModelForm):

    department = forms.ModelChoiceField(
        queryset=Department.objects.all().order_by("code"),
        required=True,
        empty_label="Select Department",
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "id": "subject-department",
            }
        ),
    )

    class Meta:

        model = Subject

        fields = [
            "department",
            "course",
            "name",
            "code",
            "semester",
        ]

        widgets = {

            "course": forms.Select(
                attrs={
                    "class": "form-control",
                    "id": "subject-course",
                }
            ),

            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter subject name",
                }
            ),

            "code": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter subject code",
                }
            ),

            "semester": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter semester",
                    "min": 1,
                    "max": 8,
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["course"].queryset = Course.objects.select_related(
            "department"
        ).order_by("code")

        # Editing an existing subject
        if self.instance.pk and self.instance.course_id:

            self.fields["department"].initial = (
                self.instance.course.department_id
            )

    def clean(self):

        cleaned_data = super().clean()

        department = cleaned_data.get("department")
        course = cleaned_data.get("course")

        if department and course:

            if course.department_id != department.id:

                raise forms.ValidationError(
                    "The selected course does not belong "
                    "to the selected department."
                )

        return cleaned_data