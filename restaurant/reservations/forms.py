from django import forms
from .models import Reservation
from datetime import date, time, datetime, timedelta

class ReservationForm(forms.ModelForm):
    OPENING_TIME = time(hour=18, minute=0)
    CLOSING_TIME = time(hour=22, minute=0)

    class Meta:
        model = Reservation
        fields = ['date', 'time', 'guests']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean_date(self):
        reservation_date = self.cleaned_data.get('date')
        if reservation_date < date.today():
            raise forms.ValidationError("Non è possibile prenotare per una data passata.")
        return reservation_date

    def clean(self):
        cleaned_data = super().clean()
        reservation_time = cleaned_data.get('time')
        
        if reservation_time and (reservation_time < self.OPENING_TIME or reservation_time > self.CLOSING_TIME):
            raise forms.ValidationError(f"Il ristorante è aperto dalle {self.OPENING_TIME.strftime('%H:%M')} alle {self.CLOSING_TIME.strftime('%H:%M')}.")

        reservation_date = cleaned_data.get('date')
        reservation_guests = cleaned_data.get('guests')

        if reservation_date and reservation_time and reservation_guests:
            MAX_CAPACITY = 50 
            
            existing_reservations = Reservation.objects.filter(
                date=reservation_date,
                time=reservation_time
            )
            
            total_guests = sum(r.guests for r in existing_reservations) + reservation_guests
            
            if total_guests > MAX_CAPACITY:
                self.add_error(None, "Siamo al completo per quest'orario. Prova un altro slot o una data diversa.")
        
        return cleaned_data