from django.db import models


class Booking(models.Model):

    bookingID = models.AutoField(primary_key=True)
    # to be added once authentication is completed
    #userID = models.ForeignKey(Showing, on_delete=models.CASCADE)
    screeningID = models.ForeignKey(Screening, on_delete=models.CASCADE)
    numTickets = models.IntegerField()
    numTotal = models.IntegerField()
    def __str__(self):
        return str(self.bookingID)
