from django.views.generic import TemplateView
# Create your views here.
from django.urls import reverse_lazy
from .models import *
from allauth.account.views import SignupView
from django.shortcuts import redirect
from .forms import CustomSignUpForm


class HomeView(TemplateView):
    template_name = 'home.html'


class CustomSignUpView(SignupView):
    form_class = CustomSignUpForm
    def get_success_url(self):
        if "/institution" in self.request.path:
            return reverse_lazy('institution_home')
        elif '/student' in self.request.path:
            return reverse_lazy('student_home')
