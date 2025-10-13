from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ReservationForm
from .models import Reservation

@login_required
def home(request):
    prenotazioni = Reservation.objects.filter(user=request.user).order_by('date', 'time')
    context = {
        'prenotazioni': [
            {
                'data': p.date,
                'ora': p.time,
                'numero_persone': p.guests
            }
            for p in prenotazioni
        ]
    }
    return render(request, 'reservations/home.html', context)

@login_required
def create_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            try:
                reservation.save()
                messages.success(request, 'Prenotazione effettuata con successo!')
                return redirect('home')
            except Exception as e:
                messages.error(request, 'Si è verificato un errore. Riprova.')
        else:

            form.instance.user = request.user
    else:
        form = ReservationForm()
    return render(request, 'reservations/create_reservation.html', {'form': form})