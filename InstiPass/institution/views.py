from django.shortcuts import render
from rest_framework import viewsets
from django.views.generic import CreateView,UpdateView,TemplateView
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from django.urls import reverse_lazy
from .models import *
from Id.models import *
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.mixins import LoginRequiredMixin
from .serializers import *
from django.shortcuts import get_object_or_404

# Create your views here.
class InstitutionViewSet(viewsets.ModelViewSet):
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer
    http_method_names = ['get','post','put','patch','delete']
    permission_classes = [IsAuthenticated]

class InstitutionSettingsViewSet(viewsets.ModelViewSet):
    queryset = InstitutionSettings.objects.all()
    serializer_class = InstitutionSettingsSerializer    
    http_method_names = ['get','post','put','patch','delete']
    permission_classes = [IsAuthenticated]

class CreateInstitution(LoginRequiredMixin,CreateView):
    success_url = reverse_lazy("institution_home")    
    model = Institution
    fields = ['name','region','county','address','email','tel','admin_email','admin_tell']
    template_name = "register_institution.html"
    login_url = "accounts/login/"
    redirect_field_name = "next"
 
   
class CreateInstitutionSettings(LoginRequiredMixin,CreateView):
    success_url = reverse_lazy("institution_home")    
    model = InstitutionSettings
    fields = ['institution','notification_pref','template','barcode','qrcode','min_admission_year']
    template_name = "register_institution_settings.html"    
    login_url = "../accounts/login/"
    redirect_field_name = "next"

class UpdateInstitution(LoginRequiredMixin,UpdateView):
    success_url = reverse_lazy("home")    
    model = Institution
    fields = ['name','region','county','address','email','tel']
    template_name = "register_institution.html"
 
class UpdateInstitutionSettings(LoginRequiredMixin,UpdateView):
    success_url = reverse_lazy("home")    
    model = InstitutionSettings
    fields = ['institution','notification_pref','template','barcode','qrcode','min_admission_year']
    template_name = "institution/"+"register_institution_settings.html"
  
class IdProcessStatsAPIView(APIView):
    def get(self, request, *args, **kwargs):
        institution = get_object_or_404(Institution,email = self.request.user.email)
        data = {
            "registered_students": Student.objects.filter(institution=institution).count(),
            "Ids_in_Queue":len([id for id in IdOnQueue.objects.all() if id.student.institution==institution]),
            "Ids_being_processed": len([id for id in IdInProcess.objects.all() if id.Id.student.institution==institution]),
            "Ids_ready": len([id for id in IdReady.objects.all() if id.Id.student.institution==institution]),
        }
        
        return Response(data=data)
        

class HomeView(TemplateView):
    template_name = 'institution_home.html'    
def custom_404_view(request, exception):
    return render(request, "404.html", status=404)

def custom_500_view(request):
    return render(request, "500.html", status=500)

def custom_403_view(request, exception):
    return render(request, "403.html", status=403)    