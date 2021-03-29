from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
# from base_app.CustomStuff import aasdasd

rout=DefaultRouter()
rout.register('image', ImageDataAPI, basename='image')

urlpatterns = [
    path('labeling/<int:pk>/', labeling_view, name='labeling'),
    path('edit_image/<int:pk>/', edit_image_data_view, name='base-panel'),
    path('upload/', upload_view, name='upload'),
    path('image_list/', list_all_view, name='listing'),
    path('user_assignment/', user_assignment_view, name='user-assignment'),
    path('panel/', Panel.as_view(), name='base-panel'),

    # path('_DEV/load_new_images/', aasdasd, name='load_new_images'),
    path('_api/roundRobin/', round_robin, name='roundRobin'),
    path('_api/next_to_label/', next_to_label, name='next_to_label'),

    path('_api/', include(rout.urls)),
    path('_api/image_list/', ImageListAPI.as_view({"get":"list"}), name='ImageListAPI'),
]
