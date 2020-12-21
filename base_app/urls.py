from django.urls import path
from base_app.views import home, about, panel, case_study, contact
from base_app.webservice import getImage, getPoints, setPoints, getImageList, getLabel, setLabel, getList

urlpatterns = [
    path('', home, name='base-home'),
    path('panel/', panel, name='base-panel'),
    path('case-study/', case_study, name='base-case-study'),
    path('about/', about, name='base-about'),
    path('contact/', contact, name='base-contact'),

    # webservice
    path('webservice/getImage/<int:patient_id>/<int:image_id>/', getImage, name='webservice-getImage'),
    path('webservice/getImage/<int:patient_id>/', getImageList, name='webservice-getImage'),
    path('webservice/getPoints/<int:patient_id>/<int:image_id>/', getPoints, name='webservice-getPoints'),
    path('webservice/setPoints/<int:patient_id>/<int:image_id>/', setPoints, name='webservice-setPoints'),

    path('webservice/getList/<int:patient_id>/', getList, name='webservice-getList'),
    path('webservice/getLabel/<int:patient_id>/<int:image_id>/', getLabel, name='webservice-getLabel'),
    path('webservice/setLabel/<int:patient_id>/<int:image_id>/', setLabel, name='webservice-setLabel'),
]