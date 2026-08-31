from django import forms

from .models import Result


class ResultForm(forms.ModelForm):

    class Meta:

        model = Result

        fields = [
            'student',
            'subject',
            'internal_marks',
            'external_marks',
        ]

        widgets = {

            'student': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),

            'subject': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),

            'internal_marks': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': 0,
                    'max': 40,
                    'placeholder': 'Enter internal marks (0-40)'
                }
            ),

            'external_marks': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': 0,
                    'max': 60,
                    'placeholder': 'Enter external marks (0-60)'
                }
            ),

        }


    # =========================
    # VALIDATE INTERNAL MARKS
    # =========================

    def clean_internal_marks(self):

        internal_marks = self.cleaned_data.get(
            'internal_marks'
        )

        if internal_marks < 0 or internal_marks > 40:

            raise forms.ValidationError(
                'Internal marks must be between 0 and 40.'
            )

        return internal_marks


    # =========================
    # VALIDATE EXTERNAL MARKS
    # =========================

    def clean_external_marks(self):

        external_marks = self.cleaned_data.get(
            'external_marks'
        )

        if external_marks < 0 or external_marks > 60:

            raise forms.ValidationError(
                'External marks must be between 0 and 60.'
            )

        return external_marks


    # =========================
    # VALIDATE DUPLICATE RESULT
    # =========================

    def clean(self):

        cleaned_data = super().clean()

        student = cleaned_data.get(
            'student'
        )

        subject = cleaned_data.get(
            'subject'
        )

        if student and subject:

            results = Result.objects.filter(
                student=student,
                subject=subject
            )

            # While editing, exclude
            # the current result
            if self.instance.pk:

                results = results.exclude(
                    pk=self.instance.pk
                )

            if results.exists():

                raise forms.ValidationError(
                    'A result already exists for this student and subject.'
                )

        return cleaned_data