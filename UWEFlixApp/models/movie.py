from django.core.validators import MinValueValidator
from django.db import models


class Movie(models.Model):
    name = models.CharField(max_length=50)
    running_time = models.DurationField(
        validators=[MinValueValidator(limit_value=1)]
    )
    description = models.TextField()
    rating = models.CharField(max_length=3)
    image = models.ImageField(upload_to='images/', blank=True, null=True, default='images/no_image_available.png')

    def __str__(self):
        return self.name
