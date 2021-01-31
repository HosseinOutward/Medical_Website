from .models import *
from rest_framework import serializers


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagePatient
        fields = ["pk", 'class_type_imag', 'label_string_imag', 'points_imag']