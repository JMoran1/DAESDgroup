from django.db import models
from django.conf import settings
from datetime import datetime
# Create your models here.



class Movie(models.Model):
    movieID = models.AutoField(primary_key=True)
    movieName = models.CharField(max_length=50)
    movieLength = models.IntegerField()
    movieDescription = models.TextField()
    movieRating = models.CharField(max_length=3)
    def __str__(self):
        return self.movieName


class Screen(models.Model):
    screenID = models.AutoField(primary_key=True)
    screenName = models.CharField(max_length=25)
    screenDesc = models.TextField(null=True, blank=True)
    screenCapacity = models.IntegerField()

    def __str__(self):
        return self.screenName

class Screening(models.Model):
    screeningID = models.AutoField(primary_key=True)
    movieID = models.ForeignKey(Movie, on_delete=models.CASCADE)
    screenID = models.ForeignKey(Screen, on_delete=models.CASCADE)
    showingTime = models.TimeField(auto_now=False, auto_now_add=False)
    showingDate = models.DateField()
    remainingSeats = models.IntegerField()

    def __str__(self):
        return str(self.screeningID) 


class Booking(models.Model):

    bookingID = models.AutoField(primary_key=True)
    # to be added once authentication is completed
    #userID = models.ForeignKey(Showing, on_delete=models.CASCADE)
    screeningID = models.ForeignKey(Screening, on_delete=models.CASCADE)
    numTickets = models.IntegerField()
    numTotal = models.IntegerField()
    def __str__(self):
        return str(self.bookingID)

class Club(models.Model):
    clubID = models.AutoField(primary_key=True)
    clubName =  models.CharField(max_length=25)
    cardNum = models.IntegerField(max_length=25)
    expDate = models.IntegerField(max_length=8)
    discountRate = models.FloatField()
    clubAddress = models.CharField(max_length=500)
    # clubContact = 
    def __str__(self):
        return str(self.clubName)

class MonthlyStatement(models.Model):
    statementID = models.AutoField(primary_key=True)
    clubID = models.ForeignKey(Club, on_delete=models.CASCADE)
    statementDate = models.DateField()
    statementAmount = models.FloatField()

    def __str__(self):
        return str(self.statementID)