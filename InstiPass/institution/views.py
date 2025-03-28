from django.shortcuts import render
from rest_framework import viewsets
from django.views.generic import CreateView,UpdateView,TemplateView
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from django.urls import reverse_lazy
from .models import *
from .serializers import *

# Create your views here.
class InstitutionViewSet(viewsets.ModelViewSet):
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer
    http_method_names = ['get','post','put','patch','delete']
    permission_classes = [IsAuthenticated,IsAdminUser]

class InstitutionSettingsViewSet(viewsets.ModelViewSet):
    queryset = InstitutionSettings.objects.all()
    serializer_class = InstitutionSettingsSerializer    
    http_method_names = ['get','post','put','patch','delete']
    permission_classes = [IsAuthenticated,IsAdminUser]

class CreateInstitution(CreateView):
    success_url = reverse_lazy("home")    
    model = Institution
    fields = ['name','region','county','address','email','tel']
    template_name = "register_institution.html"
class CreateInstitutionSettings(CreateView):
    success_url = reverse_lazy("home")    
    model = InstitutionSettings
    fields = ['institution','notification_pref','template','barcode','qrcode','min_admission_year']
    template_name = "register_institution_settings.html"    

class UpdateInstitution(UpdateView):
    success_url = reverse_lazy("home")    
    model = Institution
    fields = ['name','region','county','address','email','tel']
    template_name = "register_institution.html"
class UpdateInstitutionSettings(UpdateView):
    success_url = reverse_lazy("home")    
    model = InstitutionSettings
    fields = ['institution','notification_pref','template','barcode','qrcode','min_admission_year']
    template_name = "register_institution_settings.html"

class HomeView(TemplateView):
    template_name = 'home.html'    
def custom_404_view(request, exception):
    return render(request, "404.html", status=404)

def custom_500_view(request):
    return render(request, "500.html", status=500)

def custom_403_view(request, exception):
    return render(request, "403.html", status=403)    