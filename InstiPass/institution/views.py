from rest_framework import viewsets
from django.views.generic import CreateView,UpdateView,DeleteView,DetailView
from django.urls import reverse_lazy
from .models import *
from .serializers import *

# Create your views here.
class InstitutionViewSet(viewsets.ModelViewSet):
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer
    http_method_names = ['get','post','put','patch','delete']

class InstitutionSettingsViewSet(viewsets.ModelViewSet):
    queryset = InstitutionSettings.objects.all()
    serializer_class = InstitutionSettingsSerializer    
    http_method_names = ['get','post','put','patch','delete']

class CreateInstitution(CreateView):
    success_url = reverse_lazy("home")    
    model = Institution
    fields = ['name','region','county','address','email','tel']
    template_name = "register_institution.html"
class CreateInstitutionSettings(CreateView):
    success_url = reverse_lazy("home")    
    model = InstitutionSettings
    fields = ['institution','notification_pref','template','barcode','qrcode']
    template_name = "register_institution_settings.html"    