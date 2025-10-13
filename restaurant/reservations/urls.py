from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('prenota/', views.create_reservation, name='nuova_prenotazione'),
    path('delete/<int:reservation_id>/', views.delete_reservation, name='delete_reservation'),
    path('confirm/<int:reservation_id>/', views.confirm_reservation, name='confirm_reservation'),
]
