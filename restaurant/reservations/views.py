from django.shortcuts import render, redirect
from .forms import ReservationForm
from .models import Reservation
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    prenotazioni = Reservation.objects.filter(utente=request.user)
    return render(request, 'reservations/home.html', {'prenotazioni': prenotazioni})

@login_required
def create_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.utente = request.user
            reservation.save()
            return redirect('home')
    else:
        form = ReservationForm()
    return render(request, 'reservations/create_reservation.html', {'form': form})
