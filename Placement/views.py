from django.shortcuts import render,HttpResponse,redirect
from Registration.models import StudentRegistration
from .forms import PlacementForm
from .models import Placements

# Create your views here.

def placement(request):
   placements = Placements.objects.all()
   return render(request,'pages/placements.html',{'placements':placements})

def listplacement(request):
   placements = Placements.objects.all()
   return render(request,'admin/listplacement.html',{'placements':placements})

def addplacement(request):
   if request.method == "POST":
      form = PlacementForm(request.POST,request.FILES)
      if form.is_valid():
         form.save()
         return redirect('addplacement')
      else:
         return render(request,'addplacement.html',{'error':'Invalid detials Try again!'})
   else:
    form = PlacementForm()
   return render(request,'admin/addplacement.html',{'form':form})

