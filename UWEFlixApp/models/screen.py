from django.db import models


class Screen(models.Model):
    name = models.CharField(max_length=25)
    description = models.TextField(null=False, blank=True)
    capacity = models.IntegerField()

    def __str__(self):
        return self.name
