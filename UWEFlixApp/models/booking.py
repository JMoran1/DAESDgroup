from django.db import models


class Booking(models.Model):
    # to be added once authentication is completed
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    screening = models.ForeignKey('Screening', on_delete=models.CASCADE)
    number_of_tickets = models.IntegerField()
 
    def __str__(self):
        return str(self.id)
