from django.shortcuts import render,redirect
from django.contrib import messages
from django.views import View
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from .forms import RegisterForm, LoginForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    return render(request, 'users/home.html')

# creating class based views by this template
class RegisterView(View):
    # this defines the form type to be user, here we are using the RegisterForm we create in .forms
    form_class=RegisterForm 
    # this dictionary is used for placeholding purposes
    initial={'key':'value'}
    # this attr holds the html template for the registration form
    template_name='users/register.html'


    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='login')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)



    # this function handles the get request, that is user is asking for the registration form from the server
    # this function firstly creates an instance of the form_class and initializes the dict initial
    # this function returns the registration html template and form instance created for the user asking for registration
    def get(self,request, *args, **kwargs):
        form=self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form':form})
    


    # this function handles all the post request, that is user is submitting his credentials to the server
    def post(self, request, *args, **kwargs):

        # by the line below we create an instance of the form that is of the type of form_class, 
        # with the arguement as request.POST, the form instance created right now is filled with the data that 
        # the user submitted in the form request.POST
        form=self.form_class(request.POST)

        if form.is_valid():
            # now we check whether the form is valid, that is contains all the entries according to our form requirements

            form.save()
            # if the form is valid, we save the data in our database


            user_name=form.cleaned_data.get('username')
            # cleaned_data extracts all the data from the form, in a dictionary format, where we search for the users username


            messages.success(request,f'Account created for {user_name}')
            # display a success messgae

            return redirect(to='/')
            # redirect accordingly
        
        return render(request, self.template_name, {'form':form})
        # if the form isnt valid, a new form is shown again



class CustomLoginView(LoginView):
    form_class=LoginForm

    def form_valid(self, form):
        remember_me=form.cleaned_data.get('remember_me')

        if not remember_me:
            self.request.session.set_expiry(0)

            self.request.session.modified = True

        return super(CustomLoginView,self).form_valid(form)


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'


    email_template_name = 'users/password-reset-email.html'
    # The template used for generating the body of the email with the reset password link

    subject_template_name = 'users/password_reset_subject.txt'
    # The template used for generating the subject of the email with the reset password link


    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    # The message that will be displayed upon a successful password reset request


    success_url = reverse_lazy('home')
    # If not given any, django defaults to 'password_reset_done' after a successful password request. 
    # But I think it makes sense to just redirect the user to the home page without providing any additional template.


@login_required
def profile(request):
    return render(request, 'users/profile.html')
# The login_required decorator limits access to logged in users
# a user who isnt authenticated, tries to hit, the login_required redirects it to settings.LOGIN_URL, and then would go directly
# to the page (profile page) after authentication
