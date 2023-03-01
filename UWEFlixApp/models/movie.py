from django.core.validators import MinValueValidator
from django.db import models


class Movie(models.Model):
    name = models.CharField(max_length=50)
    minutes_long = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(limit_value=1)]
    )
    description = models.TextField()
    rating = models.CharField(max_length=3)

    def __str__(self):
        return self.name
