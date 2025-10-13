from django.db import models
from django.contrib.auth.models import User

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    
    date = models.DateField()
    time = models.TimeField()
    guests = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date', 'time']
        unique_together = ('date', 'time', 'user')

    def __str__(self):
        return f"Prenotazione di {self.user.username} per il {self.date} alle {self.time} ({self.guests} persone)"