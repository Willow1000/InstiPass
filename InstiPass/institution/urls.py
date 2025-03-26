from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register("institution",InstitutionViewSet,basename="institutionApi")
router.register("institution_settings",InstitutionSettingsViewSet,basename="institutionSettingsApi")

urlpatterns = [
    path('institution/register',CreateInstitution.as_view(),
    name="create_institution"),
    path('institution_settings/register',CreateInstitutionSettings.as_view(),name="create_institution_settings"),
    path("api/",include(router.urls))
]