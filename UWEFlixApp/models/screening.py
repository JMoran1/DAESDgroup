from django.db import models
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

    class Meta:
        ordering = ('showing_at',)
        # constraints = (
        #     models.CheckConstraint(
        #         # check=Q(club__isnull=True) ^ Q(role__in=(Role.CLUB_REP, Role.STUDENT)),
        #         check=models.Q(showing_at__gt=Screen.objects.get(id=models.F('screen'))),
        #         name='members_have_club',
        #         violation_error_message='Only Club Reps and Students must have Clubs'
        #     ),
        # )
        pass

    def __str__(self):
         return f"{self.movie} - {self.showing_at}"


def screenings_with_finish_times():
    return Screening.objects.annotate(finishing_at=models.F('showing_at') + models.F('movie__running_time'))
