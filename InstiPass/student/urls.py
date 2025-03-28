from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import *
from accounts.views import CustomSignUpView


router = DefaultRouter()
router.register('student',StudentViewSet,basename='studentApi')
urlpatterns = [
    path("",HomeView.as_view(),name='student_home'),
    path('account/signup/',CustomSignUpView.as_view(),name='student_signup'),
    path("account/",include("allauth.urls")),
    path("api/",include(router.urls)),
    path("register",CreateStudentView.as_view(),name="student_registration"),
    path("update/<int:pk>",UpdateStudentView.as_view(),name="update_student")
]