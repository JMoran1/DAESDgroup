from django.db import models
from UWEFlixApp.models import Movie, Screen

class Showing(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE)
    start_time = models.DateTimeField()

    def __str__(self):
        return f"{self.movie.name} - {self.screen.name} - {self.start_time}"
