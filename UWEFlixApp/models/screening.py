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
        return cls.objects.annotate(  # first sum up all allocated ticket types
            adult_tickets=Coalesce(Sum('booking__number_of_adult_tickets'), 0),
            child_tickets=Coalesce(Sum('booking__number_of_child_tickets'), 0),
            student_tickets=Coalesce(Sum('booking__number_of_student_tickets'), 0)
        ).annotate(  # then subtract them from Screen capacity
            _seats_remaining=F('screen__capacity') - (
                F('adult_tickets') +
                F('child_tickets') +
                F('student_tickets')
            )
        )
