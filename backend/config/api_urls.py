from rest_framework.routers import DefaultRouter

from students.views import StudentViewSet
from teachers.views import TeacherViewSet
from courses.views import (
    DepartmentViewSet,
    CourseViewSet,
    SubjectViewSet,
)
from attendance.views import AttendanceViewSet
from results.views import ResultViewSet


router = DefaultRouter()

router.register(
    r'students',
    StudentViewSet,
    basename='students'
)

router.register(
    r'teachers',
    TeacherViewSet,
    basename='teachers'
)

router.register(
    r'departments',
    DepartmentViewSet,
    basename='departments'
)

router.register(
    r'courses',
    CourseViewSet,
    basename='courses'
)

router.register(
    r'subjects',
    SubjectViewSet,
    basename='subjects'
)

router.register(
    r'attendance',
    AttendanceViewSet,
    basename='attendance'
)

router.register(
    r'results',
    ResultViewSet,
    basename='results'
)


urlpatterns = router.urls