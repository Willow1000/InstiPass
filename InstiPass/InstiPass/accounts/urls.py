from django.urls import path
from .views import *
from django.urls import include
from django.contrib.auth import views as auth_views
from .views import PasswordResetView

urlpatterns = [
    path("",HomeView.as_view(),name='home'),
    path("signup/redirect",SignupRedirectView.as_view(),name="signup_redirect"),
    path("about",AboutView.as_view(),name="about"),
    path("signup",SignUpView.as_view(),name="signup"),
    path('password-reset/', 
     PasswordResetView.as_view(

         template_name='password_reset_form.html',
         email_template_name='password_reset_email.html',
         subject_template_name='registration/password_reset_subject.txt',
        #  success_url=
     ), 
     name='password_reset'),
     path(
        'password-reset/confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='password_reset_conf.html',  # your custom template
            success_url='../../../../reset/done/'  # optional
        ),
        name='password_reset_confirm'
    ),
    path('password-reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),

    path('reset/done/', PasswordResetSuccessView.as_view(), name='password_reset_complete'),
    path("login/",LoginView.as_view(),name="login")

]
