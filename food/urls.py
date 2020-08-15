from django.contrib import admin
from django.urls import path,include
from food import views

urlpatterns=[
    path('',views.Index,name="index.html"),
    path('contact/',views.contact,name="conatct.html"),
    path('payment/',views.payment,name="payment.html"),
    path('home/',views.home,name="home.html"),
    path('loginUser/',views.loginUser,name="login.html"),
    path('register/',views.register,name="register.html"),
    path('logoutUser/',views.logoutUser,name="logout.html"),
    path('delete/',views.delet,name="delete"),
    path('add/',views.add,name="add"),
    path('addx/',views.addx,name="addx"),
    path('address/',views.addres,name="addr"),
    path('dell/',views.dell,name="addr"),
    
]