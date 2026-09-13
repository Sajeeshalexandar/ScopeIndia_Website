from django.shortcuts import render,redirect
from .models import Faq,Reviews
from .forms import FaqForm,ReviewsForm

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
    review = Reviews.objects.all()
    return render(request,'pages/reviews.html',{'review':review})





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



def addreview(request):
    if request.method == "POST":
        form = ReviewsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('reviews')
        else:
            return render(request,'pages/addreview.html',{'error':'Invalid review Try again!'})
    else:
        form = ReviewsForm()
    return render(request,'pages/addreview.html',{'form':form})