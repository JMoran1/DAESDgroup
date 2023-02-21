from django.db import models


class Club(models.Model):
    name = models.CharField(max_length=25)
    '''
    TODO: using a third party model field type for credit card details or better
    yet, something like Stripe for payments would be even better, but this'll do
    '''
    card_number = models.CharField(max_length=16)  # most are 16, Amex is 15
    card_expiry = models.DateField()
    discount_rate = models.DecimalField()
    address = models.CharField(max_length=500)
    # clubContact = 
    def __str__(self):
        return str(self.name)
