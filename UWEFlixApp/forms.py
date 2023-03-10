from django import forms
from django.contrib import admin
from django.contrib.auth.forms import AuthenticationForm
from UWEFlixApp.models import Club, Movie, Screen, User


class ClubForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ('name', 'card_number', 'card_expiry', 'discount_rate', 'address')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'card_number': forms.TextInput(attrs={'class': 'form-control'}),
            'card_expiry': forms.TextInput(attrs={'class': 'form-control'}),
            'discount_rate': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
        }


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ('name', 'minutes_long', 'rating')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'minutes_long': forms.TextInput(attrs={'class': 'form-control'}),
            'rating': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ScreenForm(forms.ModelForm):
    class Meta:
        model = Screen
        fields = ('name', 'description', 'capacity')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'capacity': forms.TextInput(attrs={'class': 'form-control'}),
        }


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

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
