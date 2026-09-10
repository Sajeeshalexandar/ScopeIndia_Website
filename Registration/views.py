from django.shortcuts import render
from .forms import StudentRegistrationForm

# Create your views here.
def registration(request):
    form = StudentRegistrationForm()
    return render(request,'pages/registration.html',{'form':form})