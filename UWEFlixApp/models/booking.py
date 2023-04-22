from django.core.validators import MinValueValidator
from django.db import models


class Booking(models.Model):
    # to be added once authentication is completed
    user = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True)
    screening = models.ForeignKey('Screening', on_delete=models.CASCADE)
    number_of_adult_tickets = models.IntegerField()
    number_of_child_tickets = models.IntegerField()
    number_of_student_tickets = models.IntegerField()
    total_price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        validators=[MinValueValidator(limit_value=0)]  # can't be negative
    )
    club = models.ForeignKey('Club', on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField(auto_now=True, blank=True, null=True, max_length=100)
 
    def __str__(self):
        return str(self.user)
