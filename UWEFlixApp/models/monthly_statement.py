from django.db import models


class MonthlyStatement(models.Model):
    statementID = models.AutoField(primary_key=True)
    clubID = models.ForeignKey('Club', on_delete=models.CASCADE)
    statementDate = models.DateField()
    statementAmount = models.FloatField()

    def __str__(self):
        return str(self.statementID)
