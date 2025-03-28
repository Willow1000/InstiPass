from django.urls import path,include
from rest_framework.routers import DefaultRouter
from django.conf.urls import handler404,handler500,handler403
from .views import *
from accounts.views import CustomSignUpView

handler404 = custom_404_view
handler403 = custom_403_view
handler500  = custom_500_view


router = DefaultRouter()
router.register("institution",InstitutionViewSet,basename="institutionApi")
router.register("institution_settings",InstitutionSettingsViewSet,basename="institutionSettingsApi")

urlpatterns = [
    path('',HomeView.as_view(),name="institution_home"),
    path('account/signup/',CustomSignUpView.as_view(),name='institution_signup'),
    path("account/",include("allauth.urls")),
    path('register',CreateInstitution.as_view(),
    name="create_institution"),
    path('settings/register',CreateInstitutionSettings.as_view(),name="create_institution_settings"),
    path("api/",include(router.urls)),
    path("update/<int:pk>",UpdateInstitution.as_view(),name="update_institution"),
    path("settings/update/<int:pk>",UpdateInstitutionSettings.as_view(),name="update_institution_settings"),
]

from InstiPass import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)