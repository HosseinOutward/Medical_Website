from django.db import models
from django.contrib.auth.models import User


class Hospital(models.Model):
    name_hosp = models.CharField(max_length=200)
    address_hosp = models.TextField(max_length=200)


class UserProfile(models.Model):
    name_prof = models.CharField(max_length=200)
    image_prof = models.ImageField(default='defaultNew.jpg', upload_to='profile_pic')
    hosp_prof = models.ManyToManyField(Hospital)
    # type_prof = models.??()

    user_prof = models.OneToOneField(User, on_delete=models.CASCADE)
