from datetime import timedelta
from math import ceil

from django.core.validators import MinValueValidator
from django.db import models



class Movie(models.Model):
    DEFAULT_IMAGE = 'images/no_image_available.png'

    name = models.CharField(max_length=50)
    running_time = models.DurationField(
        validators=[MinValueValidator(limit_value=timedelta(minutes=1))]
    )
    description = models.TextField()
    rating = models.CharField(max_length=3)
    image = models.ImageField(upload_to='images/', blank=True, null=True, default=DEFAULT_IMAGE)

    def __str__(self):
        return self.name

    @property
    def minutes_long(self):
        return str(ceil(self.running_time.total_seconds() / 60))
    
    def save(self, *args, **kwargs):
        if not self.image:
            self.image.name = self.DEFAULT_IMAGE

        super(Movie, self).save(*args, **kwargs)
