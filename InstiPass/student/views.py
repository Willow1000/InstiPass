from rest_framework import viewsets
from .models import *
from .serializers import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView,UpdateView,TemplateView
from django.urls import reverse_lazy

# Create your views here.
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
    login_url = "accounts/login/"
    redirect_field_name = "next"

class UpdateStudentView(UpdateView):
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

class HomeView(TemplateView):
    template_name = 'student_home.html'