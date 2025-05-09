from rest_framework import viewsets
from .models import *
from .serializers import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView,UpdateView,TemplateView
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.contrib.auth.views import LogoutView
from django.shortcuts import redirect



# Create your views here.
class LogoutView(LogoutView):
    next_page = reverse_lazy("login")    
    def dispatch(self, request, *args, **kwargs):
        logout(request)  # Ensure session is cleared
        return redirect(self.next_page)
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class CreateStudentView(LoginRequiredMixin,CreateView):
    template_name = 'student_registration.html'
    model = Student
    success_url = reverse_lazy("student_home")
    fields = [
    "institution",
    "reg_no",
    "first_name",
    "last_name",
    "course",
    "notification_pref",
    "admission_year",
    "email",
    "phone_number",
    "photo",
    ]
    login_url = "login"
    redirect_field_name = "next"

class UpdateStudentView(LoginRequiredMixin,UpdateView):
    template_name = 'student_registration.html'
    model = Student
    success_url = reverse_lazy("student_home")
    login_url = "login"
    redirect_field_name = "next"
    fields = [
    "reg_no",
    "first_name",
    "last_name",
    "course",
    "notification_pref",
    "admission_year",
    "email",
    "phone_number",
    "photo",
    ]

class HomeView(LoginRequiredMixin,TemplateView):
    template_name = 'student_home.html'
    login_url = "login"
    redirect_field_name = "next"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        found = Student.objects.filter(email=self.request.user.email)
        if found:
            context['exists'] = True
            context['pk'] = found[0].pk
        else:
            context['exists'] = False 

        return context       



# views.py
