from django.db import models


class Screen(models.Model):
    screenID = models.AutoField(primary_key=True)
    screenName = models.CharField(max_length=25)
    screenDesc = models.TextField(null=True, blank=True)
    screenCapacity = models.IntegerField()

    def __str__(self):
        return self.screenName
