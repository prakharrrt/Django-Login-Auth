from django.contrib import admin
from django.contrib.auth import views as auth_views

from django.urls import path
from . import views
from . import forms

urlpatterns = [
    path('', views.home, name='home'),
    path('register', views.RegisterView.as_view(),name='user-registration'),
    # .as_view() is a class method which returns a function that can be called when a request arrives for a URL matching the associated pattern.
    
    path('login', views.CustomLoginView.as_view( template_name='users/login.html',
                                           authentication_form=forms.LoginForm), name='login'),
    path('logout', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
]


