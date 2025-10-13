# reservations/urls.py (o nel tuo urls.py principale)
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('prenota/', views.create_reservation, name='create_reservation'),
]