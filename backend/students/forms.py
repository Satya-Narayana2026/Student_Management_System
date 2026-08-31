from django import forms

from .models import Student
from courses.models import Course


class StudentForm(forms.ModelForm):

    username = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter username for student login'
            }
        )
    )

    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter password for student login'
            }
        )
    )

    course = forms.ModelChoiceField(
        queryset=Course.objects.select_related(
            'department'
        ).order_by(
            'department__code',
            'code',
            'name'
        ),
        required=True,
        empty_label='Select Course',
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        )
    )

    class Meta:

        model = Student

        fields = [
            'student_id',
            'first_name',
            'last_name',
            'email',
            'phone',
            'date_of_birth',
            'gender',
            'course',
            'year',
            'address',
        ]

        widgets = {

            'student_id': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter student ID'
                }
            ),

            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter first name'
                }
            ),

            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter last name'
                }
            ),

            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter email address'
                }
            ),

            'phone': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter phone number'
                }
            ),

            'date_of_birth': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                }
            ),

            'gender': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),

            'year': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),

            'address': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter address',
                    'rows': 4
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields['course'].label_from_instance = (
            lambda course:
            f"{course.department.code} | "
            f"{course.code} | "
            f"{course.name}"
        )