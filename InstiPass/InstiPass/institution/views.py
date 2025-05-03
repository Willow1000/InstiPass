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
from django.shortcuts import get_object_or_404,redirect
import requests
import json
from django.contrib import messages

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

class CreateInstitution(CreateView):
    success_url = reverse_lazy("institution_home")    
    model = Institution
    fields = ['name','region','county','address','email','tel','admin_email','admin_tell']
    template_name = "register_institution.html"
 
   
class CreateInstitutionSettings(CreateView):
    success_url = reverse_lazy("institution_home")    
    model = InstitutionSettings
    fields = ['notification_pref','template','barcode','qrcode','min_admission_year']
    template_name = "register_institution_settings.html"    

    def form_valid(self, form):
        found = Institution.objects.filter(email = self.request.user.email)
        if found:
            form.instance.institution = found[0]
        else:
            messages.warning(message="Kindly create a profile for your institution first",request=self.request)    
            return redirect('institution_home')
        return super().form_valid(form)
 

class UpdateInstitution(UpdateView):
    success_url = reverse_lazy("home")    
    model = Institution
    fields = ['name','region','county','address','email','tel']
    template_name = "register_institution.html"
 
class UpdateInstitutionSettings(UpdateView):
    success_url = reverse_lazy("home")    
    model = InstitutionSettings
    fields = ['notification_pref','template','barcode','qrcode','min_admission_year']
    template_name = "register_institution_settings.html"
  
class IdProcessStatsAPIView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request, *args, **kwargs):
        email=self.request.GET.get("q")
        institution = get_object_or_404(Institution,email = email)
        print(email)
        data = {
            "registered_students": Student.objects.filter(institution=institution).count(),
            "Ids_in_Queue":len([id for id in IdOnQueue.objects.all() if id.student.institution==institution]),
            "Ids_being_processed": len([id for id in IdInProcess.objects.all() if id.Id.student.institution==institution]),
            "Ids_ready": len([id for id in IdReady.objects.all() if id.Id.Id.student.institution==institution]),
        }
        
        return Response(data=data)
        

class HomeView(TemplateView):
    template_name = 'institution_home.html'    

    def get_context_data(self,**kwargs):
        stats = super().get_context_data(**kwargs)
        sessionid = self.request.COOKIES.get("sessionid")
        cookies = {
            'sessionid':sessionid
        }
    
        data = json.loads(requests.get(url = f"http://127.0.0.1:8000/institution/api/institution_stats/?q={self.request.user.email}",cookies=cookies).content.decode("utf8"))
        print(requests.get(url = "http://127.0.0.1:8000/institution/api/institution_stats",cookies=cookies).content.decode("utf8"))
        stats['total'] = data.get("registered_students")
        stats['process'] = data.get("Ids_being_processed")
        stats["ready"] = data.get("Ids_ready")
        print(self.request.user.email)
        found = Institution.objects.filter(email=self.request.user.email)
        if found:
            stats['exists_institution'] = True
            stats['pk'] = found[0].pk
            settings = InstitutionSettings.objects.filter(institution = found[0])
            if settings:
                stats['exists_settings'] = True
                stats['s_pk'] = settings[0].pk

        
        return stats
def custom_404_view(request, exception):
    return render(request, "404.html", status=404)

def custom_500_view(request):
    return render(request, "500.html", status=500)

def custom_403_view(request, exception):
    return render(request, "403.html", status=403)    

