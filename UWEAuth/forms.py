from django import forms
from django.contrib import admin
from .models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ['password']

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['groups'] = User.sanitise_groups(
            cleaned_data['groups'],
            User.Role(cleaned_data['role'])
        )


class UserAdmin(admin.ModelAdmin):
    form = UserForm
