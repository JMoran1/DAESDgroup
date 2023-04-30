import hashlib

from django.core.validators import MinValueValidator
from django.db import models

from UWEAuth.models import User


class Club(models.Model):
    name = models.CharField(max_length=25)
    '''
    TODO: using a third party model field type for credit card details or better
    yet, something like Stripe for payments would be even better, but this'll do
    '''
    card_number = models.CharField(max_length=128)
    card_expiry = models.DateField()
    discount_rate = models.DecimalField(
        decimal_places=2, max_digits=4,
        validators=[MinValueValidator(limit_value=0)] # discount can't be negative
    )
    address = models.CharField(max_length=500)
    balance = models.DecimalField(decimal_places=2, max_digits=10, default=0)

    @property
    def members(self):
        """
        Returns a QuerySet of all Users who belong to this Club, regardless of
        User type.
        """
        return self.user_set.all()  # you could just user user_set directly, but this is more idiomatic

    @property
    def reps(self):
        """
        Returns a QuerySet of all Users who are representatives of this Club
        """
        return self.members.filter(role=User.Role.CLUB_REP)

    # clubContact = 
    def __str__(self):
        return str(self.name)
    
    def check_card(self, card_number):
        return self.card_number == hashlib.sha3_512(card_number.encode()).hexdigest()
