from django import forms
from .models import Faq,Reviews

class FaqForm(forms.ModelForm):
    class Meta:
        model = Faq
        fields = [
            'question',
            'answer'
        ]
        widgets = {
            'question': forms.Textarea(
                attrs= {
                    'class' : 'form-control',
                    'placeholder' : 'Enter the Question'
                }
            ),
            'answer': forms.Textarea(
                attrs= {
                    'class' : 'form-control',
                    'placeholder' : 'Enter the Answer',

                }
            ),
        }
    
class ReviewsForm(forms.ModelForm):
    class Meta:
        model = Reviews
        fields = [
            'name',
            'review'
        ]

        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Enter Your Name'
                }
            ),
            'review': forms.Textarea(
                attrs={
                    'class':'form-control',
                    'placeholder':'Enter Your Review'
                }
            ),
        }