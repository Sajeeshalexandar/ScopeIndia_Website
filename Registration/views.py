from django.shortcuts import render,redirect
from .forms import StudentRegistrationForm
from .models import StudentRegistration

# Create your views here.
def registration(request):
    if request.method == "POST":
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request,'pages/registration.html',{'success':'Registration Successfull'})
        else:
            return render(request,'pages/registration.html',{'error':'Invalid detials Try again!'})
    else:
        form = StudentRegistrationForm()
    return render(request,'pages/registration.html',{'form':form})
def registrationlist(request):
   registrationDetails = StudentRegistration.objects.all()
   return render(request,'admin/registrationlist.html',{'regDetails':registrationDetails})