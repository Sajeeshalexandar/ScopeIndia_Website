from django.shortcuts import render,redirect
from django.contrib.auth import authenticate as user_auth
from django.contrib.auth import login as user_login
from django.contrib.auth import logout as user_logout
from .forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def authentication(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = user_auth(request,username = username, password = password)
        if user is not None:
            user_login(request,user)
            return redirect('adminPanel')
        else:
            form = AuthenticationForm()
            return render(request,'admin/authentication.html',{'error':"Invalid username or password Try again!",'form':form})
    else:
        form = AuthenticationForm()
        return render(request,'admin/authentication.html',{'form':form})
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('authentication')
        else:
            return render(request,'admin/adminregister.html',{'error':"Invalid username or password",'form':form})
    else:
        form = UserCreationForm()
        return render(request,'admin/adminregister.html',{'form':form})


def logout(request):
    user_logout(request)
    return redirect('authentication')