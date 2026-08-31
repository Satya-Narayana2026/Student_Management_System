from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0004_remove_course_department"),
        ("departments", "0001_initial"),
    ]

    operations = [

        migrations.SeparateDatabaseAndState(

            # Database operation:
            # Rename the existing courses_department table
            # so the existing Department data is preserved.
            database_operations=[
                migrations.RunSQL(
                    sql="""
                        RENAME TABLE
                        courses_department
                        TO departments_department;
                    """,
                    reverse_sql="""
                        RENAME TABLE
                        departments_department
                        TO courses_department;
                    """,
                ),
            ],

            # Django model-state operations:
            # Remove Department from courses state and add it
            # to departments state without recreating the table.
            state_operations=[
                migrations.DeleteModel(
                    name="Department",
                ),
            ],
        ),

        migrations.AddField(
            model_name="course",
            name="department",
            field=__import__(
                "django.db.models",
                fromlist=["ForeignKey"]
            ).ForeignKey(
                blank=True,
                null=True,
                on_delete=__import__(
                    "django.db.models",
                    fromlist=["PROTECT"]
                ).PROTECT,
                related_name="courses",
                to="departments.department",
            ),
        ),
    ]