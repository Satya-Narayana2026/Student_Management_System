from django import forms
from .models import Attendance


class AttendanceForm(forms.ModelForm):

    class Meta:
        model = Attendance

        fields = [
            "student",
            "date",
            "status",
            "remarks",
        ]

        widgets = {

            "student": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),

            "date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control"
                }
            ),

            "status": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),

            "remarks": forms.TextInput(
                attrs={
                    "placeholder": "Optional remarks",
                    "class": "form-control"
                }
            ),

        }