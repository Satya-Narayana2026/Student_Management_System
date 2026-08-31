from django.db import models

from courses.models import Course


class Subject(models.Model):

    course = models.ForeignKey(
        Course,
        on_delete=models.PROTECT,
        related_name="subjects"
    )

    name = models.CharField(
        max_length=100
    )

    code = models.CharField(
        max_length=20
    )

    semester = models.PositiveIntegerField(
        default=1
    )

    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=["course", "code"],
                name="unique_subject_code_per_course"
            )
        ]

        ordering = [
            "course__code",
            "semester",
            "code"
        ]

    def __str__(self):
        return f"{self.code} - {self.name}"