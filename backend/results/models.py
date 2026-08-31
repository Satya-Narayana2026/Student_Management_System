from django.db import models

from students.models import Student
from subjects.models import Subject


class Result(models.Model):

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="results"
    )

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="results"
    )

    internal_marks = models.PositiveIntegerField(
        default=0
    )

    external_marks = models.PositiveIntegerField(
        default=0
    )

    total_marks = models.PositiveIntegerField(
        default=0
    )

    grade = models.CharField(
        max_length=5,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )


    class Meta:

        constraints = [

            models.UniqueConstraint(
                fields=[
                    "student",
                    "subject"
                ],
                name="unique_student_subject_result"
            )

        ]


    def save(self, *args, **kwargs):

        self.total_marks = (
            self.internal_marks +
            self.external_marks
        )

        if self.total_marks >= 90:

            self.grade = "A+"

        elif self.total_marks >= 80:

            self.grade = "A"

        elif self.total_marks >= 70:

            self.grade = "B"

        elif self.total_marks >= 60:

            self.grade = "C"

        elif self.total_marks >= 50:

            self.grade = "D"

        else:

            self.grade = "F"

        super().save(
            *args,
            **kwargs
        )


    def __str__(self):

        return f"{self.student} - {self.subject}"