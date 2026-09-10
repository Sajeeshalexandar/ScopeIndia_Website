from django.db import models
from Courses.models import CourseList


class StudentRegistration(models.Model):

    GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    ]

    TRAINING_MODE_CHOICES = [
        ("online", "Live Online"),
        ("classroom", "Classroom"),
    ]

    LOCATION_CHOICES = [
        ("technopark", "Technopark TVM"),
        ("thampanoor", "Thampanoor TVM"),
        ("kochi", "Kochi"),
        ("nagercoil", "Nagercoil"),
        ("online", "Online"),
    ]

    TIMING_CHOICES = [
        ("8am-10am", "Between 8am - 10am"),
        ("9am-1pm", "Between 9am - 1pm"),
        ("1pm-6pm", "Between 1pm - 6pm"),
        ("6pm-10pm", "Between 6pm - 10pm"),
    ]

    full_name = models.CharField(max_length=100)

    date_of_birth = models.DateField()

    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)

    educational_qualification = models.CharField(max_length=100, blank=True)

    mobile = models.CharField(max_length=15)

    email = models.EmailField()

    guardian_name = models.CharField(max_length=100, blank=True)

    guardian_occupation = models.CharField(max_length=100, blank=True)

    guardian_mobile = models.CharField(max_length=15, blank=True)

    course = models.ForeignKey(CourseList, on_delete=models.PROTECT)

    training_mode = models.CharField(max_length=20, choices=TRAINING_MODE_CHOICES)

    location = models.CharField(max_length=20, choices=LOCATION_CHOICES)

    preferred_timings = models.JSONField(default=list)

    address = models.TextField(blank=True)

    country = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.full_name
