from django.db import models


class Syllabus(models.Model):
    syllabus_name = models.CharField(max_length=100)
    syllabus_description = models.TextField(blank=True)

    def __str__(self):
        return self.syllabus_name


class CourseList(models.Model):
    course_name = models.CharField(max_length=100)
    course_duration = models.CharField(max_length=100)
    course_description = models.TextField()

    course_syllabus = models.ManyToManyField(
        Syllabus,
        blank=True,
        related_name="courses"
    )

    def __str__(self):
        return self.course_name