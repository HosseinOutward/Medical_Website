from django.contrib import admin
from .models import UserProfile, Hospital


admin.site.register(Hospital)
admin.site.register(UserProfile)