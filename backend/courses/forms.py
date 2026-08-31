from django import forms

from .models import Course
from departments.models import Department


class CourseForm(forms.ModelForm):

    class Meta:

        model = Course

        fields = [
            "department",
            "name",
            "code",
            "duration_years",
        ]

        widgets = {

            "department": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),

            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter course name"
                }
            ),

            "code": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter course code"
                }
            ),

            "duration_years": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1,
                    "max": 10,
                    "placeholder": "Enter duration in years"
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["department"].queryset = (
            Department.objects.all().order_by("code")
        )