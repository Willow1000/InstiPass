from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView,UpdateView,DeleteView,DetailView
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth import logout
from .forms import LoginForm
from django.shortcuts import redirect
from institution.models import *
import requests
from student.models import *
from django.shortcuts import get_object_or_404
import json
from django.contrib import messages


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
    
class InstituttionsView(UserPassesTestMixin,LoginRequiredMixin,ListView):
        model = Institution
        template_name = "admin_institution.html"
        context_object_name = "institutions"
        login_url = reverse_lazy('adminLogin')

        def get_queryset(self):
            query = self.request.GET.get('q')
            if query:
                return Institution.objects.filter(name__icontains=query) | Institution.objects.filter(region__icontains=query) | Institution.objects.filter(county__icontains=query)
            return Institution.objects.all()
        def test_func(self):
            return self.request.user.is_superuser
        
class InstitutionadminView(UserPassesTestMixin,LoginRequiredMixin,DetailView):
    model = Institution
    template_name = "admin_institution_detail.html"
    context_object_name = "institution"
    login_url = reverse_lazy('adminLogin')
    
    def get_context_data(self, **kwargs):
        sessionid = self.request.COOKIES.get("sessionid")
        cookies = {
            'sessionid':sessionid
        }
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get("pk")
        institution = get_object_or_404(Institution,id = pk)
        context['settings'] = InstitutionSettings.objects.filter(institution=institution).first()
    
        data = json.loads(requests.get(url = f"http://127.0.0.1:8000/institution/api/institution_stats/?q={institution.email}",cookies=cookies).content.decode("utf8"))
        print(requests.get(url = "http://127.0.0.1:8000/institution/api/institution_stats",cookies=cookies).content.decode("utf8"))
        context['total'] = data.get("registered_students")
        context['process'] = data.get("Ids_being_processed")
        context["ready"] = data.get("Ids_ready")
        
        
        return context
    def test_func(self):
            return self.request.user.is_superuser

class StudentsAdminView(UserPassesTestMixin,LoginRequiredMixin,ListView):
    model = Student
    template_name = "admin_student.html"
    login_url = reverse_lazy('adminLogin')
    def get_context_data(self, **kwargs):
        email = self.request.GET.get("q")
        query = self.request.GET.get('querry')
        institution = Institution.objects.filter(email=email).first()
       
        context = super().get_context_data(**kwargs)
        if query:
            context["students"] = Student.objects.filter(last_name__icontains=query , institution=institution) | Student.objects.filter(first_name__icontains=query,institution=institution) | Student.objects.filter(status__icontains = query, institution=institution) | Student.objects.filter(email__icontains = query,institution=institution) | Student.objects.filter(phone_number__icontains=query, institution=institution)
            if not context['students']:
                messages.warning(message = "No results match your search",request = self.request)
        elif Student.objects.filter(institution=institution):
            context['students'] = Student.objects.filter(institution=institution)    

        else:
            context['no_students'] = True    
        context["institution"] = institution

        return context
    def test_func(self):
        return self.request.user.is_superuser

class DeleteInstitutionView(UserPassesTestMixin,LoginRequiredMixin,DeleteView):
    model = Institution
    success_url = reverse_lazy("institutions_admin")
    def test_func(self):
        return self.request.user.is_superuser

class DeleteStudentView(UserPassesTestMixin,LoginRequiredMixin,DeleteView):
    model = Student

    def test_func(self):

        return self.request.user.is_superuser
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        return next_url 

        