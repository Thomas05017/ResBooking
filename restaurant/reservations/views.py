from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistrationForm
from .forms import ReservationForm
from .models import Reservation
from django.contrib.auth import login
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registrazione completata con successo!')
            return redirect('home')
        else:
            messages.error(request, 'Errore nella registrazione. Controlla i dati inseriti.')
    else:
        form = RegistrationForm()

    return render(request, 'registration/register.html', {'form': form})


@login_required
def home(request):
    if request.user.is_staff:
        prenotazioni = Reservation.objects.all().order_by('date', 'time')
    else:
        prenotazioni = Reservation.objects.filter(user=request.user).order_by('date', 'time')

    return render(request, 'reservations/home.html', {
        'prenotazioni': prenotazioni
    })


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
        form = ReservationForm()

    return render(request, 'reservations/create_reservation.html', {'form': form})


@login_required
def delete_reservation(request, reservation_id):
    if not request.user.is_staff:
        return HttpResponseForbidden("Non hai i permessi per eliminare questa prenotazione.")
    
    reservation = get_object_or_404(Reservation, id=reservation_id)
    reservation.delete()
    messages.success(request, 'Prenotazione eliminata con successo.')
    return redirect('home')

@login_required
def confirm_reservation(request, reservation_id):
    if not request.user.is_staff:
        return HttpResponseForbidden("Non hai i permessi per confermare questa prenotazione.")
    
    reservation = get_object_or_404(Reservation, id=reservation_id)
    reservation.confirmed = True
    reservation.save()
    messages.success(request, 'Prenotazione confermata.')
    return redirect('home')
