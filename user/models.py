from django.db import models
from django.contrib.auth.models import User


# class Hospital(models.Model):
#     name_hosp = models.CharField(max_length=200)
#     address_hosp = models.TextField(max_length=200)


class UserProfile(models.Model):
    image_profile = models.ImageField(default=r'profile_pic/default.jpg', upload_to='profile_pic')
    # hosp_prof = models.ManyToManyField(Hospital)
    # type_prof = models.CharField()

    user_profile = models.OneToOneField(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super(UserProfile, self).save(*args, **kwargs)
        from PIL.Image import open as open_image
        if self.image_profile.name!=r'profile_pic/default.jpg':
            img = open_image(self.image_profile.file)
            img.thumbnail((256, 256))
            img.save(self.image_profile.path)
