from django import forms
from .models import StudentRegistration


class StudentRegistrationForm(forms.ModelForm):

    preferred_timings = forms.MultipleChoiceField(
        choices=StudentRegistration.TIMING_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:

        model = StudentRegistration

        fields = [
            "full_name",
            "date_of_birth",
            "gender",
            "educational_qualification",
            "mobile",
            "email",
            "guardian_name",
            "guardian_occupation",
            "guardian_mobile",
            "course",
            "training_mode",
            "location",
            "preferred_timings",
            "address",
            "country",
        ]

        widgets = {

            "full_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your full name",
                }
            ),

            "date_of_birth": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "gender": forms.RadioSelect(),

            "educational_qualification": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your qualification",
                }
            ),

            "mobile": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your mobile number",
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your email",
                }
            ),

            "guardian_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter guardian name",
                }
            ),

            "guardian_occupation": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter guardian occupation",
                }
            ),

            "guardian_mobile": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter guardian mobile",
                }
            ),

            "course": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "training_mode": forms.RadioSelect(),

            "location": forms.RadioSelect(),

            "address": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your address",
                    "rows": 2,
                }
            ),

            "country": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter your country",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["course"].empty_label = None
        self.fields["gender"].choices = StudentRegistration.GENDER_CHOICES
        self.fields["training_mode"].choices = StudentRegistration.TRAINING_MODE_CHOICES
        self.fields["location"].choices = StudentRegistration.LOCATION_CHOICES