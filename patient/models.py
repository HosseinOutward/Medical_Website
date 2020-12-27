from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.postgres.fields import ArrayField
from user.models import Hospital
import json


class Patient(models.Model):
    name_pati = models.CharField(max_length=200)
    description_pati = models.TextField()
    date_pati = models.DateTimeField(default=timezone.now)

    hospital_pati = models.ForeignKey(Hospital, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('patient-detail', kwargs={'pk': self.pk})


class ImagePatient(models.Model):
    image_imag = models.FileField(upload_to='')
    class_type_imag = models.CharField(max_length=9,
            choices=[(class_obj["name"], class_obj["name"]) for class_obj in json.load(open("Laminitis/etc/Image_class.json"))])

    label_string_imag = models.TextField(default="NotSetYet")
    points_imag = ArrayField(ArrayField(models.FloatField(), size=2))

    last_modifier_imag = models.IntegerField(null=True)
    creator_imag = models.IntegerField(null=True)

    last_edited_imag = models.DateTimeField(default=timezone.now)

    patient_imag = models.ForeignKey(Patient, null=True, on_delete=models.SET_NULL)

    def get_absolute_url(self):
        return reverse('base-panel')




