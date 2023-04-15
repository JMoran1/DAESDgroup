from datetime import timedelta
from math import ceil

from django.core.validators import MinValueValidator
from django.db import models


class MinutesField(models.DurationField):
    """
    Subclass of Django's DurationField that is stepped to a minute-resolution.
    """
    @staticmethod
    def minutes_only(td: timedelta) -> timedelta:
        return timedelta(seconds=ceil(td.total_seconds() / 60))

    def to_python(self, value):
        duration = super().to_python(value)
        # duration should now be a timedelta, possibly with seconds
        # round it up to the nearest minute
        return self.minutes_only(duration)

    def get_prep_value(self, value):
        # round up to the nearest minute before storing
        return super().get_prep_value(minutes_only(value))

    def value_to_string(self, obj):
        return self.minutes_only(obj).total_seconds() // 60

    def to_representation(self, value):
        return self.minutes_only(value).total_seconds() // 60

class Movie(models.Model):
    name = models.CharField(max_length=50)
    running_time = MinutesField(
        validators=[MinValueValidator(limit_value=timedelta(minutes=1))]
    )
    description = models.TextField()
    rating = models.CharField(max_length=3)
    image = models.ImageField(upload_to='images/', blank=True, null=True, default='images/no_image_available.png')

    def __str__(self):
        return self.name
