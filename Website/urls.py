from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('about/',views.about,name='about'),
    path('placements/',views.placements,name='placements'),
    path('faq/',views.faq,name='faq'),
    path('reviews/',views.reviews,name='reviews'),
    path('contact/',views.contact,name='contact'),
    
]