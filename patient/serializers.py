from .models import *
from rest_framework import serializers


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagePatient
        fields = ["pk"]+["image_imag", "real_id_imag"]+col_names+["label_data_imag"]
        extra_kwargs = {
            'pk': {'read_only': True},
            'label_data_imag': {'read_only': True},
        }


class ImageSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model = ImagePatient
        fields = col_names+["label_data_imag"]