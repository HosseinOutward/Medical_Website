from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField


class Patient(models.Model):
    name_pati = models.CharField(max_length=200)
    description_pati = models.TextField()
    date_pati = models.DateTimeField(default=timezone.now)

    doctor_pati = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('patient-detail', kwargs={'pk': self.pk})


class ImagePatient(models.Model):
    # dicomInfo_imag = models.TextField()
    image_imag = models.FileField(upload_to='')

    MONTH_CHOICES = (("class1", "class1"), ("class2", "class2"), )
    class_type_imag = models.CharField(max_length=9, choices=MONTH_CHOICES, default="JANUARY")
    label_string_imag = models.TextField(default="NotSetYet")

    points_imag = ArrayField(ArrayField(models.FloatField(), size=2))

    patient_imag = models.ForeignKey(Patient, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('patient-detail', kwargs={'pk': self.patient_imag.pk})

