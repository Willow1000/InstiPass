from django.views.generic import TemplateView
# Create your views here.
from django.urls import reverse_lazy
from .models import *
from django.shortcuts import redirect

class HomeView(TemplateView):
    template_name = 'home.html'



