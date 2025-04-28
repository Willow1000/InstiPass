from django.urls import path
from .views import *

urlpatterns = [
    path("",HomeView.as_view(),name='home'),
    path("signup/redirect",SignupRedirectView.as_view(),name="signup_redirect"),
    path("about",AboutView.as_view(),name="about")
]
