from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):

    help = "Create user roles and assign permissions"


    def handle(self, *args, **kwargs):

        # =========================
        # CREATE GROUPS
        # =========================

        admin_group, created = Group.objects.get_or_create(
            name="Admin"
        )

        teacher_group, created = Group.objects.get_or_create(
            name="Teacher"
        )

        student_group, created = Group.objects.get_or_create(
            name="Student"
        )


        # =========================
        # REMOVE STAFF GROUP
        # =========================

        Group.objects.filter(
            name="Staff"
        ).delete()


        # =========================
        # ADMIN PERMISSIONS
        # =========================

        admin_group.permissions.set(
            Permission.objects.all()
        )


        # =========================
        # TEACHER PERMISSIONS
        # =========================

        teacher_permissions = Permission.objects.filter(
            content_type__app_label__in=[
                "students",
                "attendance",
                "results",
                "courses",
            ]
        )

        teacher_group.permissions.set(
            teacher_permissions
        )


        # =========================
        # STUDENT PERMISSIONS
        # =========================

        student_permissions = Permission.objects.filter(
            content_type__app_label__in=[
                "students",
                "attendance",
                "results",
                "courses",
            ],
            codename__startswith="view_"
        )

        student_group.permissions.set(
            student_permissions
        )


        self.stdout.write(
            self.style.SUCCESS(
                "Roles and permissions created successfully!"
            )
        )