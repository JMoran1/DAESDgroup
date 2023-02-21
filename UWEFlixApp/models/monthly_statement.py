from django.db import models


class MonthlyStatement(models.Model):
    club = models.ForeignKey('Club', on_delete=models.CASCADE)
    date = models.DateField()
    amount = models.DecimalField()

    def __str__(self):
        return str(self.id)
