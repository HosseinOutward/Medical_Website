from .models import *
from rest_framework import serializers


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagePatient
        fields = ["pk","assigned_doc_imag"]+["image_imag", "real_id_imag"]+col_names+["label_data_imag"]
        extra_kwargs = {
            'pk': {'read_only': True},
            'label_data_imag': {'read_only': True},
            'assigned_doc_imag': {'read_only': True},

            'bronchial_graph': {'read_only': True},
            'interstitial_graph': {'read_only': True},
            'alveolar_graph': {'read_only': True},
            'cardiomegaly_graph': {'read_only': True},
            'bulge_graph': {'read_only': True},
            'trachea_deviation': {'read_only': True},
        }


class ImageSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model = ImagePatient
        fields = col_names+["label_data_imag"]