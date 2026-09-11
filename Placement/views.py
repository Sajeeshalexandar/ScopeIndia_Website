from django.shortcuts import render,HttpResponse

# Create your views here.

def placement(request):
   return render(request,'pages/placements.html')