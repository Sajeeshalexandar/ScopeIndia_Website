from django.shortcuts import render,redirect
from .models import Faq
from .forms import FaqForm

# Create your views here.

def home(request):
    

    return render(request,'pages/home.html')
def about(request):
    return render(request,'pages/about.html')
def placements(request):
    return render(request,'pages/placements.html')
def contact(request):
    return render(request,'pages/contact.html')
def faq(request):
    faqs = Faq.objects.all()
    return render(request,'pages/faq.html',{'faqs':faqs})
def reviews(request):
    return render(request,'pages/reviews.html')



def addfaq(request):
    if request.method == "POST":
        form = FaqForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('addfaq')
        else:
            return render(request,'admin/addfaq.html',{'error':'Invalid Question or Answer Try again!'})
    else:
        form = FaqForm()
    return render(request,'admin/addfaq.html',{'form': form})
def listfaq(request):
    faqs = Faq.objects.all()
    return render(request,'admin/listfaq.html',{'faqs': faqs})
