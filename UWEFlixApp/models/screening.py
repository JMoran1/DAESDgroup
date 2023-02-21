from django.db import models


class Screening(models.Model):
    screeningID = models.AutoField(primary_key=True)
    movieID = models.ForeignKey('Movie', on_delete=models.CASCADE)
    screenID = models.ForeignKey('Screen', on_delete=models.CASCADE)
    showingTime = models.TimeField(auto_now=False, auto_now_add=False)
    showingDate = models.DateField()
    remainingSeats = models.IntegerField()

    def __str__(self):
        return str(self.screeningID) 
