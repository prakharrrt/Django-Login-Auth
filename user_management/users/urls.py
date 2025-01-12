from django.contrib import admin
from django.contrib.auth import views as auth_views
from users.views import ResetPasswordView
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

        path('password-reset', ResetPasswordView.as_view(), name='password_reset'),
    # matches urls for password-reset

    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    # matches for urls such as {{ protocol }}://{{ domain }}{% url 'password_reset_confirm' uidb64=uid token=token %}


    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),

    path('profile', views.profile, name='users-profile'),
    path('password-change', views.ChangePasswordView.as_view(), name='password_change')
]


