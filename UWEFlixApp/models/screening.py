from django.db import models
from django.db.models import Count
from UWEFlixApp.models import Movie, Screen


class Screening(models.Model):
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
    screen = models.ForeignKey('Screen', on_delete=models.CASCADE)
    showing_at = models.DateTimeField(auto_now=False, auto_now_add=False)
    
    @classmethod
    def with_seats_remaining(cls):
        """
        Returns new QuerySet with all Screening objects, annotated with a
        subquery giving the number of remaining bookable seats per Screening
        """
        pass

    @classmethod
    def bookable(cls):
        """
        Returns a new QuerySet of all bookable Screenings (those that have some
        seats remaining and which didn't start in the past)
        """
        pass

    @property
    def seats_remaining(self):
        return self.booking_set.annotate(seats_allocated=Count('number_of_tickets'))

    @property
    def is_bookable(self):
        return self.seats_remaining > 0

    def __str__(self):
        return f"{self.movie.name} - {self.screen.name} - {self.showing_at}"
