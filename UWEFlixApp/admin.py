from django.contrib import admin
from .forms import UserAdmin
from .models import User, Screening, Screen, Movie

admin.site.register(User, UserAdmin)
admin.site.register(Screen)
admin.site.register(Movie)
admin.site.register(Screening)