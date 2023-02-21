from django.db import models


class Movie(models.Model):
    name = models.CharField(max_length=50)
    duration = models.DurationField()
    description = models.TextField()
    rating = models.CharField(max_length=3)

    def __str__(self):
        return self.name
