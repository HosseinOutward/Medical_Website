from base_app.views import home, about, case_study, contact
from django.urls import path


urlpatterns = [
    path('', home, name='base-home'),
    path('case-study/', case_study, name='base-case-study'),
    path('about/', about, name='base-about'),
    path('contact/', contact, name='base-contact'),
]
