from django.db import models
from django.contrib.auth.models import User

from Registration.models import StudentRegistration
from Courses.models import CourseList








class StudentAccount(models.Model):

    student = models.OneToOneField(
        StudentRegistration,
        on_delete=models.CASCADE,
        related_name="student_account"
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="student_account"
    )

    is_first_login = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.student.full_name


class PickedCourse(models.Model):

    student = models.ForeignKey(
        StudentAccount,
        on_delete=models.CASCADE,
        related_name="picked_courses"
    )

    course = models.ForeignKey(
        CourseList,
        on_delete=models.PROTECT,
        related_name="picked_by_students"
    )

    signed_up_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["student", "course"],
                name="unique_student_course"
            )
        ]

    def __str__(self):
        return f"{self.student.student.full_name} - {self.course.course_name}"