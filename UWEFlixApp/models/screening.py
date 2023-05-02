from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Case, F, IntegerField, Sum, Q, When
from django.db.models.functions import Coalesce

from UWEFlixApp.models import Booking, Movie, Screen


class Screening(models.Model):
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
    screen = models.ForeignKey('Screen', on_delete=models.CASCADE)
    showing_at = models.DateTimeField(auto_now=False, auto_now_add=False)

    def __str__(self):
         return f"{self.movie} - {self.showing_at}"

    @classmethod
    def objects_with_seats_remaining(cls):
        return cls.objects.annotate(
            _seats_remaining=F('screen__capacity') - (
                # subtract the sum of each ticket type across all bookings for this screening from the screen capacity
                Case(
                    When(
                        booking__status__in=(Booking.Status.ACTIVE, Booking.Status.CANCELLATION_REQUESTED),
                        then=Coalesce(Sum('booking__number_of_adult_tickets'), 0)
                    ),
                    default=0,
                    output_field=IntegerField()
                ) +
                Case(
                    When(
                        booking__status__in=(Booking.Status.ACTIVE, Booking.Status.CANCELLATION_REQUESTED),
                        then=Coalesce(Sum('booking__number_of_child_tickets'), 0)
                    ),
                    default=0,
                    output_field=IntegerField()
                ) +
                Case(
                    When(
                        booking__status__in=(Booking.Status.ACTIVE, Booking.Status.CANCELLATION_REQUESTED),
                        then=Coalesce(Sum('booking__number_of_student_tickets'), 0)
                    ),
                    default=0,
                    output_field=IntegerField()
                )
            )
        )

    @property
    def seats_remaining(self):
        """
        Reuse existing queryset wrapper.
        
        A bit awkward but less code duplication.
        """
        return Screening.objects_with_seats_remaining(
        ).filter(id=self.id).values_list('_seats_remaining')[0][0]

    @classmethod
    def objects_with_finish_times(cls):
        """
        Ideally, we'd turn this into a custom Manager, alas!
        """
        # return cls.objects.prefetch_related('movie').annotate(
        return cls.objects.annotate(
            _finishing_at=(models.F('showing_at') + models.F('movie__running_time'))
        )

    @property
    def finishing_at(self):
        return self.showing_at + self.movie.running_time

    @property
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
        if self.clashes_with_others:
            raise ValidationError('Screening would clash with other Screenings')
        return super().clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
