from django.db import models
from institution.models import Institution
from django.core.exceptions import ValidationError
# Create your models here.
class Student(models.Model):
    STATUS_CHOICES = (('application_received',"Applicated has been received"),("id_processing","Your ID is being Processed"),("id_ready","Your ID is ready"))
    NOTIFICATION_CHOICES = [
    ("email", "Email"),
    ("sms", "SMS"),
    ("both","Both")
    ]
    institution = models.OneToOneField(Institution,on_delete=models.CASCADE)
    ADMISSION_YEAR_CHOICES=()
    reg_no = models.CharField(max_length=50)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    notification_pref = models.CharField(max_length=10,choices=NOTIFICATION_CHOICES)
    admission_year = models.CharField(choices=ADMISSION_YEAR_CHOICES,max_length=100)
    email = models.EmailField(max_length=100)
    phone_number = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='student_photo')
    staus = models.CharField(choices=STATUS_CHOICES,max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        Institution_year = self.institution.min_admission_year

        if self.admission_year < Institution_year:
            raise ValidationError('Your admission year makes you ineligible to make this application')
        return super().clean()
    

    def __str__(self):
        return self.institution,self.pk