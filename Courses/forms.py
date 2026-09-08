from django import forms
from .models import CourseList, Syllabus


class CourseForm(forms.ModelForm):

    class Meta:
        model = CourseList

        fields = [
            "course_name",
            "course_duration",
            "course_description",
            "course_syllabus",
        ]

        widgets = {
            "course_description": forms.Textarea(
                attrs={
                    "rows": 5
                }
            ),

            "course_syllabus": forms.CheckboxSelectMultiple(),
        }


class SyllabusForm(forms.ModelForm):

    class Meta:
        model = Syllabus

        fields = [
            "syllabus_name",
            "syllabus_description",
        ]

        widgets = {
            "syllabus_description": forms.Textarea(
                attrs={
                    "rows": 5
                }
            ),
        }