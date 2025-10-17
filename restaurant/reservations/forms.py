from django import forms
from django.core.exceptions import ValidationError
from .models import Reservation
from datetime import date, time, datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email'
    }))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Conferma Password'}),
        }


class ReservationForm(forms.ModelForm):
    OPENING_TIME = time(hour=18, minute=0)
    CLOSING_TIME = time(hour=22, minute=0)
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
                'step': '3600'  # Intervalli di 1 ora
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
        return cleaned_data