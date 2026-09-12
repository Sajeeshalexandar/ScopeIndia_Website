from django import forms
from .models import Placements


class PlacementForm(forms.ModelForm):
    class Meta:
        model = Placements
        fields = [
            'name',
            'role',
            'company_name',
            'image',
        ]

        widgets = {
            'name' : forms.TextInput(
                attrs={
                    'class' : 'form-control',
                    'placeholder' : 'Enter the Name',
                }
            ),
            'role' : forms.TextInput(
                attrs={
                    'class' : 'form-control',
                    'placeholder':'Enter the Role',
                }
            ),
            'company_name' : forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Enter the Company Name'
                }
            ),
            'image': forms.ClearableFileInput(
                attrs = {
                    'class' : 'form-control'
                }
            )
        }