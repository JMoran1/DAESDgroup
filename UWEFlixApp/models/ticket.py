from django.core.validators import MinValueValidator
from django.db import models

class Ticket(models.Model):
    type = models.SlugField(max_length=50, unique=True)
    price = models.DecimalField(
        max_digits=5, decimal_places=2,
        validators=[MinValueValidator(limit_value=0)] # price can't be negative
    )

    def __str__(self):
        return '{} Ticket'.format(self.type.capitalize())
