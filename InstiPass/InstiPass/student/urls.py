from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import *
from django.contrib.auth.views import PasswordResetView

from django.urls import path



router = DefaultRouter()
router.register('student',StudentViewSet,basename='studentApi')
urlpatterns = [
    path("",HomeView.as_view(),name='student_home'),
    path("api/",include(router.urls)),
    path("logout",LogoutView.as_view(),name="logout"),
    path("register",CreateStudentView.as_view(),name="student_registration"),
    

    path("update/<int:pk>",UpdateStudentView.as_view(),name="update_student")
]







