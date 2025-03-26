from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("account/",include("allauth.urls")),
    path("",include("accounts.urls")),
    path("",include('institution.urls')),
    path("",include('student.urls')),
]
