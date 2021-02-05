from django.db import models
from django.urls import reverse
import json


categ_file=json.load(open(r"Laminitis/etc/category_classes.json"))
col_names=[col_n for col_n in categ_file]

# import csv
# my_dict = {c:[cc for cc in categ_file[c]] for c in categ_file}
# from itertools import zip_longest
# with open('mycsvfile.csv', 'w') as f:
#     w = csv.writer(f)
#     w.writerow(col_names)
#     for v in zip_longest(*list(my_dict.values())):
#         w.writerow(v)

class ImagePatient(models.Model):
    image_imag = models.FileField(upload_to='')

    # generating col according to values in json file
    for col_n in col_names:
        exec(col_n + " = models.CharField(max_length=15, "
            "choices=[list(reversed(class_obj)) for class_obj in categ_file[col_n].items()])")

    label_data_imag = models.TextField(blank=True, null=True)
    # points_imag = models.BooleanField(ArrayField(models.FloatField(), size=2))
    #
    # last_modifier_imag = models.IntegerField(null=True)
    # creator_imag = models.IntegerField(null=True)
    #
    # last_edited_imag = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return reverse('base-panel')




