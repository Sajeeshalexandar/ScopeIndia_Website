from django.shortcuts import render,HttpResponse
from Registration.models import StudentRegistration

# Create your views here.

def placement(request):
   return render(request,'pages/placements.html')
# def addplacement(request):
