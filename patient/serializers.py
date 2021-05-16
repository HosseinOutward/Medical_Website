from .models import *
from rest_framework import serializers
from base_app.CustomStuff import is_labeled


class ImageSerializer(serializers.ModelSerializer):
    has_label = serializers.SerializerMethodField('is_labeled_seri')

    def is_labeled_seri(self, image_imag):
        return is_labeled(image_imag)

    class Meta:
        model = ImagePatient
        fields = ["pk", "image_imag", "thumbnail_imag", "owner_name_imag",
                  "pet_name_imag", "real_id_imag", "real_id_count_imag",
                  "real_time_imag", "label_data_imag", "assigned_doc_imag","has_label"]+col_names
        extra_kwargs = {
            'pk': {'read_only': True},
            'thumbnail_imag': {'read_only': True},
            'label_data_imag': {'read_only': True},
            'assigned_doc_imag': {'read_only': True},
            "has_label": {'read_only': True},
        }


class ImageSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model = ImagePatient
        fields = ["owner_name_imag", "pet_name_imag", "real_id_imag",
                  "real_id_count_imag", "real_time_imag", "label_data_imag",
                  "assigned_doc_imag", "last_edited_by_imag"]+col_names
