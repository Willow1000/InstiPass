from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import ListView,UpdateView,DeleteView,DetailView
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth import logout
from .forms import LoginForm
from django.shortcuts import redirect


# Create your views here.
# class AdminHome()
class AdminLogin(LoginView):
    form_class = LoginForm
    template_name = "admin_login.html"
    
    redirect_authenticated_user = False

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and user.is_superuser:
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)