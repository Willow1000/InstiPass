from django.dispatch import receiver
from student.models import *
from django.core.mail import send_mail
from .models import IdInProcess,IdReady
from django.db.models.signals import post_save

@receiver(post_save,sender=IdInProcess,dispatch_uid = 'notify_student_and_update_process_status')
def id_processing_update(sender,instance,created,**kwargs):
    Student.objects.filter(id=instance.Id.student.id).update(status="id_processing")
    send_mail(
        "Your Id is in the processing stage",
            "Keep up the patience",
            "admin@django.com",
            [instance.Id.student.email],
            fail_silently=False
    )
@receiver(post_save,sender=IdReady,dispatch_uid = 'notify_student_and_update_ready_status')
def id_ready_update(sender,instance,created,**kwargs):
    Student.objects.filter(id=instance.Id.student.id).update(status="id_ready")
    send_mail(
        "Your Id is ready",
            "Thank you for your patience",
            "admin@django.com",
            [instance.Id.student.email],
            fail_silently=False
    )



