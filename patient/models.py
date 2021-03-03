from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
import json
from Medical_Website.settings import BASE_DIR
from os.path import join as path_join


categ_file=json.load(open(path_join(BASE_DIR,"Medical_Website","etc","category_classes.json")))
col_names=[col_n for col_n in categ_file]


class ImagePatient(models.Model):
    image_imag = models.FileField(upload_to='patient_images')
    thumbnail_imag = models.FileField(upload_to=path_join('patient_images','thumbnail'))
    owner_name_imag = models.CharField(max_length=20, blank=True, null=True)
    pet_name_imag = models.CharField(max_length=20, blank=True, null=True)
    animal_type = models.IntegerField(blank=True, null=True)
    real_id_imag = models.IntegerField(blank=True, null=True)
    real_id_count_imag = models.IntegerField(blank=True, null=True)
    real_time_imag = models.DateTimeField(blank=True, null=True)
    label_data_imag = models.TextField(blank=True, null=True)

    # generating col according to values in json file
    for col_n in col_names:
        exec(col_n + " = models.IntegerField(null=True, "
                "choices=[list(reversed(class_obj)) "
                "for class_obj in categ_file[col_n].items()])")

    assigned_doc_imag = models.ForeignKey(User, on_delete=models.SET_NULL,
                            blank=True, null=True, related_name='assigned_doc_imag')

    last_edited_time_imag = models.DateTimeField(null=True)
    last_edited_by_imag = models.ForeignKey(User, on_delete=models.SET_NULL,
                            blank=True, null=True, related_name='last_edited_by_imag')

    def get_absolute_url(self):
        return reverse('labeling', kwargs={'pk': self.pk, 'slug': self.slug})

    def save(self, *args, **kwargs):
        # thumbnail
        from PIL.Image import open as open_image
        from Medical_Website.settings import MEDIA_ROOT
        if self.thumbnail_imag.name == "":
            upload_to_path=path_join(ImagePatient.thumbnail_imag.field.upload_to,
                                        "thumbnail"+self.image_imag.name.split("\\")[-1])

            img = open_image(self.image_imag.file)
            img.thumbnail((64, 64))
            img.save(path_join(MEDIA_ROOT,upload_to_path))
            self.thumbnail_imag=upload_to_path

        # last edited time
        last_edited_time_imag = timezone.now()

        super(ImagePatient, self).save(*args, **kwargs)
