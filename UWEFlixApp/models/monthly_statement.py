from django.db import models


class MonthlyStatement(models.Model):
    club = models.ForeignKey('Club', on_delete=models.CASCADE)
    date = models.DateField()
    amount = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return str(self.id)
