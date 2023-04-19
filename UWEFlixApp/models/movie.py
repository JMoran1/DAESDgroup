from django.core.validators import MinValueValidator
from django.db import models
from django.conf import settings
import os
from django.core.files import File


class Movie(models.Model):
    name = models.CharField(max_length=50)
    minutes_long = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(limit_value=1)]
    )
    description = models.TextField()
    rating = models.CharField(max_length=3)
    image = models.ImageField(upload_to='images/', blank=True, null=True, default='images/no_image_available.png')

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.image:
            self.image.name = 'images/no_image_available.png'

        super(Movie, self).save(*args, **kwargs)
