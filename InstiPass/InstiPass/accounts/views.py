from django.views.generic import TemplateView
# Create your views here.
from django.urls import reverse_lazy
from .models import *
from django.views.generic.edit import FormView
from accounts.models import User
from django.contrib import messages
from .forms import SignUpForm,LoginForm
# from allauth.account.views import SignupView
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
# Django core
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from accounts.forms import PasswordResetForm

# Authentication
from django.contrib.auth.tokens import default_token_generator

# Translation (for `_("Password reset")`)
from django.utils.translation import gettext_lazy as _

# Your password reset form (custom)
 # Adjust the import path based on your project

# Optional: Mixin for password reset views (only if used in your base view)
from django.contrib.auth.views import PasswordContextMixin

# Optional: Custom decorator (define or import accordingly)
# from your_project.decorators import login_not_required  # Change this to your actual path

class SignupRedirectView(TemplateView):
    template_name = "signup_redirect.html"

class HomeView(TemplateView):
    template_name = 'home.html'

class AboutView(TemplateView):
    template_name = "about.html"



class SignUpView(CreateView):
    
    template_name = 'signup.html'
    form_class = SignUpForm
    success_url = reverse_lazy('signup_redirect')  # e.g., 'login' or dashboard

    

class LoginView(LoginView):
    form_class = LoginForm
    template_name = 'login.html'
    # redirect_authenticated_user = True
    next_page= reverse_lazy('home')

class PasswordResetDoneView(TemplateView):
    template_name = 'done.html'

class PasswordResetSuccessView(TemplateView):
    template_name = "succsseful_reset.html"


# @method_decorator(login_not_required, name="dispatch")
class PasswordResetView(PasswordContextMixin, FormView):
    email_template_name = "password_reset_email.html"
    extra_email_context = None
    form_class = PasswordResetForm
    from_email = None
    html_email_template_name = None
    subject_template_name = "password_reset_subject.txt"
    success_url = reverse_lazy("password_reset_done")
    template_name = "password_reset_form.html"
    title = _("Password reset")
    token_generator = default_token_generator

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        opts = {
            "use_https": self.request.is_secure(),
            "token_generator": self.token_generator,
            "from_email": self.from_email,
            "email_template_name": self.email_template_name,
            "subject_template_name": self.subject_template_name,
            "request": self.request,
            "html_email_template_name": self.html_email_template_name,
            "extra_email_context": self.extra_email_context,
        }
        form.save(**opts)
        return super().form_valid(form)    