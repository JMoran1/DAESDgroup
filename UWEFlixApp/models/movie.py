from django.db import models


class Movie(models.Model):
    movieID = models.AutoField(primary_key=True)
    movieName = models.CharField(max_length=50)
    movieLength = models.IntegerField()
    movieDescription = models.TextField()
    movieRating = models.CharField(max_length=3)
    def __str__(self):
        return self.movieName
