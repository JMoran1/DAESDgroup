from django import forms
from .models import Club, Movie, Screen

class ClubForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ('name', 'card_number', 'card_expiry', 'discount_rate', 'address')

        
class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ('name', 'duration', 'rating')

class ScreenForm(forms.ModelForm):
    class Meta:
        model = Screen
        fields = ('name','description', 'capacity')