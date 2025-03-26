from django.db import models
from institution.models import Institution
# Create your models here.
class Student(models.Model):
    STATUS_CHOICES = ()
    institution = models.ForeignKey(Institution,on_delete=models.CASCADE)
    ADMISSION_YEAR_CHOICES=()
    reg_no = models.CharField(max_length=50)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    admission_year = models.CharField(choices=ADMISSION_YEAR_CHOICES,max_length=100)
    email = models.EmailField(max_length=100)
    photo = models.ImageField(upload_to='student_photo')
    staus = models.CharField(choices=STATUS_CHOICES,max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)