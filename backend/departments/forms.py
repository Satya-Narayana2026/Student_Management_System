from django import forms

from .models import Department


class DepartmentForm(forms.ModelForm):

    class Meta:

        model = Department

        fields = [
            "name",
            "code",
        ]

        widgets = {

            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter department name"
                }
            ),

            "code": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter department code"
                }
            ),
        }