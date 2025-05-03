from django.urls import path,include
from rest_framework.routers import DefaultRouter
from django.conf.urls import handler404,handler500,handler403
from .views import *
from InstiPass import settings
from django.conf.urls.static import static

handler404 = custom_404_view
handler403 = custom_403_view
handler500  = custom_500_view


router = DefaultRouter()
router.register("institution",InstitutionViewSet,basename="institutionApi")
router.register("institution_settings",InstitutionSettingsViewSet,basename="institutionSettingsApi")

urlpatterns = [
    path('',HomeView.as_view(),name="institution_home"),
    path("accounts/",include("allauth.urls"),name="accounts"),
    path('accounts/',include('django.contrib.auth.urls')),
    path('register',CreateInstitution.as_view(),
    name="create_institution"),
    path('settings/register',CreateInstitutionSettings.as_view(),name="create_institution_settings"),
    path("api/",include(router.urls)),
    path("api/institution_stats/",IdProcessStatsAPIView.as_view(),name="id_process_stats"),
    path("update/<int:pk>",UpdateInstitution.as_view(),name="update_institution"),
    path("settings/update/<int:pk>",UpdateInstitutionSettings.as_view(),name="update_institution_settings"),
]


if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)