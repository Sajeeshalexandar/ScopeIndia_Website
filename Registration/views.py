
from django.contrib.auth.decorators import login_required

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from .forms import StudentRegistrationForm
from .models import StudentRegistration

from StudentLogin.models import StudentAccount


def registration(request):

    if request.method == "POST":

        form = StudentRegistrationForm(request.POST)

        if form.is_valid():

            # Save registration details
            student = form.save()

            # Create Django User
            user = User.objects.create_user(
                username=student.email,
                email=student.email,
                password=None
            )

            # Make sure this is a normal student account
            user.is_staff = False
            user.is_superuser = False
            user.save()

            # Create StudentAccount
            StudentAccount.objects.create(
                student=student,
                user=user,
                is_first_login=True
            )

            return render(
                request,
                "pages/registration.html",
                {
                    "success": "Registration Successful"
                }
            )

        else:

            return render(
                request,
                "pages/registration.html",
                {
                    "form": form,
                    "error": "Invalid details. Try again!"
                }
            )

    else:

        form = StudentRegistrationForm()

    return render(
        request,
        "pages/registration.html",
        {
            "form": form
        }
    )
@login_required
def registrationlist(request):
   registrationDetails = StudentRegistration.objects.all()
   return render(request,'admin/registrationlist.html',{'regDetails':registrationDetails})