from django.db import models


class Club(models.Model):
    clubID = models.AutoField(primary_key=True)
    clubName =  models.CharField(max_length=25)
    cardNum = models.IntegerField()
    expDate = models.DateField()
    discountRate = models.FloatField()
    clubAddress = models.CharField(max_length=500)
    # clubContact = 
    def __str__(self):
        return str(self.clubName)
