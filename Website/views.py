from django.shortcuts import render

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
    return render(request,'pages/faq.html')
def reviews(request):
    return render(request,'pages/reviews.html')

