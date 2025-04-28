from django.urls import path
from .views import AdminLogin

urlpatterns = [
    path("/login",AdminLogin.as_view(),name="adminLogin")
]
