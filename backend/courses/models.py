from django.db import models

from departments.models import Department


class Course(models.Model):

    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="courses"
    )

    name = models.CharField(
        max_length=100
    )

    code = models.CharField(
        max_length=20
    )

    duration_years = models.PositiveIntegerField(
        default=4
    )

    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=["department", "code"],
                name="unique_course_code_per_department"
            )
        ]

        ordering = [
            "department__code",
            "code"
        ]

    def __str__(self):

        return f"{self.code} - {self.name}"