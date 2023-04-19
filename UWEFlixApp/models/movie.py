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
        # Check if the image field is empty
        if not self.image:
            # Set the image field back to its default value
            default_image_path = os.path.join(settings.MEDIA_ROOT, 'images', 'no_image_available.png')
            self.image.save('no_image_available.png', File(open(default_image_path, 'rb')))

        super(Movie, self).save(*args, **kwargs)
