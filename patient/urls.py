from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

rout=DefaultRouter()
rout.register('image', ImageDataAPI, basename='image')

urlpatterns = [
    path('_api/', include(rout.urls)),
    path('labeling/<int:pk>', LabelingView.as_view(), name='labeling'),
    path('panel/', Panel.as_view(), name='base-panel'),
    path('upload/', UploadView.as_view(), name='upload'),
]
