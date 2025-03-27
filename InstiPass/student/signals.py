from django.dispatch import receiver
from .models import *
from Id.models import IdOnQueue
from django.db.models.signals import post_save
from django.core.mail import send_mail

@receiver(post_save,sender=Student,dispatch_uid="update_status")
def application_received(sender,instance,created,**kwargs):
    Student.objects.filter(id=instance.id).update(status="application_received")
    IdOnQueue.objects.create(student = Student.objects.get(id=instance.id))
    send_mail(
            "We have received your application. Hang tight as we work on it",
            "It will be ready in no time.",
            "admin@django.com",
            [instance.email],
            fail_silently=False
        )