from django.db import models


class Screening(models.Model):
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
    screen = models.ForeignKey('Screen', on_delete=models.CASCADE)
    showing_at = models.DateTimeField(auto_now=False, auto_now_add=False)
    '''
    TODO: it might be better to instead create a method which returns the number
    of seats remaining by querying the total number of seats for the screen and
    subtracting the total number of places across all bookings for the screening
    '''
    seats_remaining = models.IntegerField()

    def __str__(self):
        return str(self.screeningID) 
