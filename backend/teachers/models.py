from django.db import models
from django.contrib.auth.models import User


class Teacher(models.Model):

    # Login account
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="teacher_profile"
    )

    # Department
    department = models.ForeignKey(
        "departments.Department",
        on_delete=models.PROTECT,
        related_name="teachers"
    )

    # Subjects teaches by this teacher
    subjects = models.ManyToManyField(
        "subjects.Subject",
        blank=True,
        related_name="teachers"
    )

    # Teacher information
    teacher_id = models.CharField(
        max_length=20,
        unique=True
    )

    first_name = models.CharField(
        max_length=100
    )

    last_name = models.CharField(
        max_length=100
    )

    email = models.EmailField(
        unique=True
    )

    phone = models.CharField(
        max_length=15
    )

    designation = models.CharField(
        max_length=100
    )

    qualification = models.CharField(
        max_length=150
    )

    joining_date = models.DateField()

    address = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return (
            f"{self.teacher_id} - "
            f"{self.first_name} {self.last_name}"
        )