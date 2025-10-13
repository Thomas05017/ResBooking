from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('prenota/', views.create_reservation, name='nuova_prenotazione'),
]
