from django.urls import path

from .views import *
urlpatterns = [
    path("/login",AdminLogin.as_view(),name="adminLogin"),
    path("/institutions",InstituttionsView.as_view(),name="institutions_admin"),
    path("/institution/<int:pk>", InstitutionadminView.as_view(), name="institution_admin_detail"),
    path("/logout",LogoutView.as_view(),name="adminLogout"),
]

