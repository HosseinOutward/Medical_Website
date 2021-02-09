from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ImagePatient


@receiver(post_save, sender=ImagePatient)
def edit_assigned_doc(sender, instance, created, **kwargs):
    if created:
        image_list = ImagePatient.objects.all()
        for img in image_list: pass

        chosen_doc=None
        instance.assigned_doc_imag = chosen_doc
        instance.save()
