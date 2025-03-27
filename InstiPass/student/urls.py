from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('student',StudentViewSet,basename='studentApi')
urlpatterns = [
    path("api/",include(router.urls)),
    path("student/register",CreateStudentView.as_view(),name="student_registration")
]