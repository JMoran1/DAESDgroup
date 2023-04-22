from django.db import models
from django.db.models import F, Sum
from django.db.models.functions import Coalesce
from UWEFlixApp.models import Movie, Screen


class Screening(models.Model):
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
    screen = models.ForeignKey('Screen', on_delete=models.CASCADE)
    showing_at = models.DateTimeField(auto_now=False, auto_now_add=False)

    @property
    def seats_remaining(self):
        """
        Reuse existing queryset wrapper.
        
        A bit awkward but less code duplication.
        """
        return Screening.objects_with_seats_remaining(
        ).filter(id=self.id).values_list('_seats_remaining')[0][0]

    def __str__(self):
         return f"{self.movie} - {self.showing_at}"

    @classmethod
    def objects_with_seats_remaining(cls):
        return cls.objects.annotate(
            _seats_remaining=F('screen__capacity') - (
                # subtract the sum of each ticket type across all bookings for this screening from the screen capacity
                Coalesce(Sum('booking__number_of_adult_tickets'), 0) +
                Coalesce(Sum('booking__number_of_child_tickets'), 0) +
                Coalesce(Sum('booking__number_of_student_tickets'), 0)
            )
        )
