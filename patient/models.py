from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
import json


categ_file=json.load(open(r"Medical_Website/etc/category_classes.json"))
col_names=[col_n for col_n in categ_file]


class ImagePatient(models.Model):
    image_imag = models.FileField(upload_to='')
    real_id_imag = models.IntegerField()
    label_data_imag = models.TextField(blank=True, null=True)

    # generating col according to values in json file
    for col_n in col_names:
        exec(col_n + " = models.IntegerField(null=True, "
            "choices=[list(reversed(class_obj)) "
            "for class_obj in categ_file[col_n].items()])")

    assigned_doc_imag = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    last_labeled_imag = models.DateTimeField(null=True)

    def get_absolute_url(self):
        return reverse('labeling', kwargs={'pk': self.pk, 'slug': self.slug})

