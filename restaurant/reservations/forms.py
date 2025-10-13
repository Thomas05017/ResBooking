from django import forms
from django.core.exceptions import ValidationError
from .models import Reservation
from datetime import date, time, datetime

class ReservationForm(forms.ModelForm):
    OPENING_TIME = time(hour=18, minute=0)
    CLOSING_TIME = time(hour=22, minute=0)
    MAX_CAPACITY = 50
    MIN_GUESTS = 1
    MAX_GUESTS = 20

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = Reservation
        fields = ['date', 'time', 'guests']
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'min': date.today().isoformat()
            }),
            'time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control',
                'step': '1800'  # Intervalli di 30 minuti
            }),
            'guests': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 20
            })
        }
        labels = {
            'date': 'Data della prenotazione',
            'time': 'Orario',
            'guests': 'Numero di ospiti'
        }

    def clean_date(self):
        reservation_date = self.cleaned_data.get('date')
        if not reservation_date:
            raise ValidationError("La data è obbligatoria.")
        
        if reservation_date < date.today():
            raise ValidationError("Non è possibile prenotare per una data passata.")
        
        return reservation_date

    def clean_guests(self):
        guests = self.cleaned_data.get('guests')
        if not guests:
            raise ValidationError("Il numero di ospiti è obbligatorio.")
        
        if guests < self.MIN_GUESTS:
            raise ValidationError(f"Il numero minimo di ospiti è {self.MIN_GUESTS}.")
        
        if guests > self.MAX_GUESTS:
            raise ValidationError(f"Il numero massimo di ospiti per prenotazione è {self.MAX_GUESTS}.")
        
        return guests

    def clean_time(self):
        reservation_time = self.cleaned_data.get('time')
        if not reservation_time:
            raise ValidationError("L'orario è obbligatorio.")
        
        if reservation_time < self.OPENING_TIME or reservation_time > self.CLOSING_TIME:
            raise ValidationError(
                f"Il ristorante è aperto dalle {self.OPENING_TIME.strftime('%H:%M')} "
                f"alle {self.CLOSING_TIME.strftime('%H:%M')}."
            )
        
        return reservation_time

    def clean(self):
        cleaned_data = super().clean()
        reservation_date = cleaned_data.get('date')
        reservation_time = cleaned_data.get('time')
        reservation_guests = cleaned_data.get('guests')

        if reservation_date and reservation_time and reservation_guests:
            user_has_reservation = Reservation.objects.filter(
                user=self.instance.user if hasattr(self.instance, 'user') else None,
                date=reservation_date,
                time=reservation_time
            )
            
            if self.instance.pk:
                user_has_reservation = user_has_reservation.exclude(pk=self.instance.pk)
            
            if user_has_reservation.exists():
                raise ValidationError(
                    "Hai già una prenotazione per questa data e orario. "
                    "Non puoi prenotare due volte nello stesso slot."
                )
            
            existing_reservations = Reservation.objects.filter(
                date=reservation_date,
                time=reservation_time
            )
            
            if self.instance.pk:
                existing_reservations = existing_reservations.exclude(pk=self.instance.pk)
            
            total_guests = sum(r.guests for r in existing_reservations) + reservation_guests
            
            if total_guests > self.MAX_CAPACITY:
                available_seats = self.MAX_CAPACITY - sum(r.guests for r in existing_reservations)
                if available_seats > 0:
                    raise ValidationError(
                        f"Siamo quasi al completo per quest'orario. "
                        f"Posti disponibili: {available_seats}. "
                        f"Prova un altro slot o una data diversa."
                    )
                else:
                    raise ValidationError(
                        "Siamo al completo per quest'orario. "
                        "Prova un altro slot o una data diversa."
                    )
        
        return cleaned_data