from django import forms


from django import forms
from Registration.models import StudentRegistration


class StudentProfileForm(forms.ModelForm):

    class Meta:
        model = StudentRegistration

        fields = [
            "full_name",
            "date_of_birth",
            "gender",
            "educational_qualification",
            "mobile",
            "guardian_name",
            "guardian_occupation",
            "guardian_mobile",
            "training_mode",
            "location",
            "preferred_timings",
            "address",
            "country",
        ]

        widgets = {
            "full_name": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "date_of_birth": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date"
                }
            ),

            "gender": forms.RadioSelect(),

            "educational_qualification": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "mobile": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "guardian_name": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "guardian_occupation": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "guardian_mobile": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "training_mode": forms.RadioSelect(),

            "location": forms.RadioSelect(),

            "address": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3
                }
            ),

            "country": forms.TextInput(
                attrs={
                    "class": "form-control"
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["preferred_timings"] = forms.MultipleChoiceField(
            choices=StudentRegistration.TIMING_CHOICES,
            widget=forms.CheckboxSelectMultiple,
            required=False,
            initial=self.instance.preferred_timings
        )