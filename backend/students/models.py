from django.db import models
from courses.models import Course
from django.contrib.auth.models import User

class Student(models.Model):


    user = models.OneToOneField(
    User,
    on_delete=models.CASCADE,
    null=True,
    blank=True,
    related_name="student_profile"
    )

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    YEAR_CHOICES = [
        (1, 'First Year'),
        (2, 'Second Year'),
        (3, 'Third Year'),
        (4, 'Fourth Year'),
    ]

    student_id = models.CharField(
        max_length=20,
        unique=True
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    email = models.EmailField(unique=True)

    phone = models.CharField(max_length=15)

    date_of_birth = models.DateField()

    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.PROTECT,
        related_name='students'
    )

    year = models.PositiveIntegerField(
        choices=YEAR_CHOICES
    )

    address = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.student_id} - {self.first_name} {self.last_name}"