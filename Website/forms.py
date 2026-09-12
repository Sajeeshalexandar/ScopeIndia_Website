from django import forms
from .models import Faq

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
