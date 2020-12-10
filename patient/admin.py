from django.contrib import admin
from .models import Patient, ImagePatient

admin.site.register(Patient)
admin.site.register(ImagePatient)
