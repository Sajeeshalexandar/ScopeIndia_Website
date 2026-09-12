from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('about/',views.about,name='about'),
    path('faq/',views.faq,name='faq'),
    path('reviews/',views.reviews,name='reviews'),
    path('contact/',views.contact,name='contact'),




    path('addfaq/',views.addfaq,name='addfaq'),
    path('listfaq/',views.listfaq,name='listfaq')
]