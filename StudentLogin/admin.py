from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import StudentAccount, PickedCourse


@admin.register(StudentAccount)
class StudentAccountAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "user",
        "is_first_login",
        "created_at",
    )

    list_filter = (
        "is_first_login",
    )

    search_fields = (
        "student__full_name",
        "student__email",
        "user__username",
        "user__email",
    )


@admin.register(PickedCourse)
class PickedCourseAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "course",
        "signed_up_date",
    )

    search_fields = (
        "student__student__full_name",
        "student__student__email",
        "course__course_name",
    )

    list_filter = (
        "course",
    )