from django.contrib import admin
from .forms import UserAdmin
from .models import User

admin.site.register(User, UserAdmin)
