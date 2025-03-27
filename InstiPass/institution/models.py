from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from django.utils.timezone import now

# Create your models here.
class Institution(models.Model):
    REGION_CHOICES = [
    ("Central", "Central"),
    ("Coast", "Coast"),
    ("Eastern", "Eastern"),
    ("Nairobi", "Nairobi"),
    ("North Eastern", "North Eastern"),
    ("Nyanza", "Nyanza"),
    ("Rift Valley", "Rift Valley"),
    ("Western", "Western"),
]

    COUNTY_CHOICES = [
    ("Baringo", "Baringo"),
    ("Bomet", "Bomet"),
    ("Bungoma", "Bungoma"),
    ("Busia", "Busia"),
    ("Elgeyo Marakwet", "Elgeyo Marakwet"),
    ("Embu", "Embu"),
    ("Garissa", "Garissa"),
    ("Homa Bay", "Homa Bay"),
    ("Isiolo", "Isiolo"),
    ("Kajiado", "Kajiado"),
    ("Kakamega", "Kakamega"),
    ("Kericho", "Kericho"),
    ("Kiambu", "Kiambu"),
    ("Kilifi", "Kilifi"),
    ("Kirinyaga", "Kirinyaga"),
    ("Kisii", "Kisii"),
    ("Kisumu", "Kisumu"),
    ("Kitui", "Kitui"),
    ("Kwale", "Kwale"),
    ("Laikipia", "Laikipia"),
    ("Lamu", "Lamu"),
    ("Machakos", "Machakos"),
    ("Makueni", "Makueni"),
    ("Mandera", "Mandera"),
    ("Marsabit", "Marsabit"),
    ("Meru", "Meru"),
    ("Migori", "Migori"),
    ("Mombasa", "Mombasa"),
    ("Murang'a", "Murang'a"),
    ("Nairobi", "Nairobi"),
    ("Nakuru", "Nakuru"),
    ("Nandi", "Nandi"),
    ("Narok", "Narok"),
    ("Nyamira", "Nyamira"),
    ("Nyandarua", "Nyandarua"),
    ("Nyeri", "Nyeri"),
    ("Samburu", "Samburu"),
    ("Siaya", "Siaya"),
    ("Taita Taveta", "Taita Taveta"),
    ("Tana River", "Tana River"),
    ("Tharaka Nithi", "Tharaka Nithi"),
    ("Trans Nzoia", "Trans Nzoia"),
    ("Turkana", "Turkana"),
    ("Uasin Gishu", "Uasin Gishu"),
    ("Vihiga", "Vihiga"),
    ("Wajir", "Wajir"),
    ("West Pokot", "West Pokot"),
    ]


    name = models.CharField(max_length=100)
    region = models.CharField(max_length=100,choices=REGION_CHOICES)
    county = models.CharField(max_length=100,choices=COUNTY_CHOICES)
    address = models.CharField(max_length=100)
    email = models.EmailField()
    tel = models.CharField(max_length=70)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class InstitutionSettings(models.Model):
    NOTIFICATION_CHOICES = [
    ("email", "Email"),
    ("sms", "SMS"),
    ("both","Both")
]
    qrcode = models.BooleanField()
    barcode = models.BooleanField(default=True)
    institution = models.OneToOneField(Institution,on_delete=models.CASCADE)  
    min_admission_year = models.IntegerField(validators=[MinValueValidator(2020),MaxValueValidator(now().year)])
    notification_pref = models.CharField(choices=NOTIFICATION_CHOICES,max_length=100)
    template = models.ImageField(upload_to="institution_template",null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class InstitutionAdmin(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone_number = models.CharField(max_length=100)   
