from django.contrib import admin
from .models import Screening, Screen, Movie

admin.site.register(Screen)
admin.site.register(Movie)
admin.site.register(Screening)
