from django import forms
from .models import Club, Movie, Screen

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
