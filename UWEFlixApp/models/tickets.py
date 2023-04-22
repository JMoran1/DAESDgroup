from django.core.validators import MinValueValidator
from django.db import models

class Ticket(models.Model):
    ticket_type = models.CharField(max_length=50)
    price = models.DecimalField(
        max_digits=5, decimal_places=2,
        validators=[MinValueValidator(limit_value=0)] # price can't be negative
    )

    def __str__(self):
        return self.ticket_type
