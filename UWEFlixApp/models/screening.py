from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q

from UWEFlixApp.models import Movie, Screen


class Screening(models.Model):
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
    screen = models.ForeignKey('Screen', on_delete=models.CASCADE)
    showing_at = models.DateTimeField(auto_now=False, auto_now_add=False)
    '''
    TODO: it might be better to instead create a method which returns the number
    of seats remaining by querying the total number of seats for the screen and
    subtracting the total number of places across all bookings for the screening
    '''
    seats_remaining = models.IntegerField(default=0)

    def __str__(self):
         return f"{self.movie} - {self.showing_at}"

    @classmethod
    def objects_with_finish_times(cls):
        """
        Ideally, we'd turn this into a custom Manager, alas!
        """
        return cls.objects.prefetch_related('movie').annotate(
            _finishing_at=(models.F('showing_at') + models.F('movie__running_time'))
        )

    @property
    def finishing_at(self):
        return self.showing_at + self.movie.running_time

    def clashes_with_others(self):
        """
        Returns True if this Screening clashes with others, that is to say, if
        there is at least one other Screening for the same Screen as this one,
        whose time period of showing overlaps with this one's
        """
        return Screening.objects_with_finish_times().filter(screen=self.screen).filter(
            # these queries take care of "inside" and "front" or "back" overlaps
            (~Q(_finishing_at__lte=self.showing_at) & Q(_finishing_at__lte=self.finishing_at)) |
            (~Q(showing_at__gte=self.finishing_at) & Q(showing_at__gte=self.showing_at)) |
            # this query takes care of "outside" overlaps
            Q(showing_at__lte=self.showing_at, _finishing_at__gte=self.finishing_at)
            # TODO: not sure if we need to provide the inverse of the first two terms in the orientation of the last one?
        )

    def clean(self, *args, **kwargs):
        """
        Override .clean() to force validation to make sure Screenings do not clash
        """
        if self.clashes_with_others():
            raise ValidationError('Screening would clash with other Screenings')
        return super().clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
