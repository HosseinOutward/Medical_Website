from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

rout=DefaultRouter()
rout.register('image', ImageDataAPI, basename='image')

urlpatterns = [
    path('labeling/<int:pk>', labeling_view, name='labeling'),
    path('upload/', upload_view, name='upload'),
    path('image_list/', list_all_view, name='listing'),
    path('user_assignment/', user_assignment_view, name='user-assignment'),
    path('panel/', Panel.as_view(), name='base-panel'),

    path('roundRobin/', round_robin, name='roundRobin'),

    path('_api/', include(rout.urls)),
    path('_api/image_list/', ImageListAPI.as_view({"get":"list"}), name='ImageListAPI'),
]
