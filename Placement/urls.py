from django.urls import path
from . import views


urlpatterns =[
    path('',views.placement,name='placement'),


    path('addplacement/',views.addplacement,name='addplacement'),
    path('listplacement/',views.listplacement,name='listplacement'),


]