from django.urls import path,include
from rest_framework.routers import DefaultRouter
from django.conf.urls import handler404,handler500,handler403
from .views import *

handler404 = custom_404_view
handler403 = custom_403_view
handler500  = custom_500_view


router = DefaultRouter()
router.register("institution",InstitutionViewSet,basename="institutionApi")
router.register("institution_settings",InstitutionSettingsViewSet,basename="institutionSettingsApi")

urlpatterns = [
    path('institution/register',CreateInstitution.as_view(),
    name="create_institution"),
    path('institution_settings/register',CreateInstitutionSettings.as_view(),name="create_institution_settings"),
    path("api/",include(router.urls))
]

from InstiPass import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)