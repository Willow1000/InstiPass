from django.db.models.signals import post_save
from .models import *
from django.dispatch import receiver
from django.core.mail import send_mail


@receiver(post_save,sender=User,dispatch_uid = "send_welcome_email")
def welcome_mail(sender,instance,created,**kwargs):
    if created:
        if instance.role == "institution_admin":
            send_mail(
            "Welcome",
            f"Thank for signing up as an institution admin for",
            "admin@django.com",
            [instance.email],
            fail_silently=False
        )
        send_mail(
            "Welcome",
            "Thank for signing up",
            "admin@django.com",
            [instance.email],
            fail_silently=False
        )