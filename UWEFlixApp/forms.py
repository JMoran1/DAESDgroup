from django import forms
from django.contrib import admin
from django.contrib.auth.forms import AuthenticationForm
from UWEFlixApp.models import Club, Movie, Screen, User
from .check_luhn import check_luhn
from datetime import datetime

class ClubForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ('name', 'card_number', 'card_expiry', 'discount_rate', 'address')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'card_number': forms.TextInput(attrs={'class': 'form-control'}),
            'card_expiry': forms.TextInput(attrs={'class': 'form-control', 'type': 'date'}),
            'discount_rate': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    error_css_class = 'text-danger'

    def clean_card_number(self):
        card_number = self.cleaned_data['card_number']
        if not check_luhn(card_number):
            raise forms.ValidationError("Card number is not valid")
        return card_number
    
    def clean_card_expiry(self):
        expiry = self.cleaned_data['card_expiry']
        if expiry < datetime.datetime.now():
            raise forms.ValidationError("Card has expired")
        return expiry


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ('name', 'minutes_long', 'rating', 'image')

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
    def clean_name(self):
            name = self.cleaned_data['name']
            if len(name) < 1:
                raise forms.ValidationError("Screen name must be at greater than 0 characters long")
            return name

    def clean_capacity(self):
        capacity = self.cleaned_data['capacity']
        if capacity < 1:
            raise forms.ValidationError("Capacity must be greater than 0")
        return capacity


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

class ClubTopUpForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.TextInput(attrs={'class': 'form-control'}))
    card_number = forms.CharField(max_length=16, widget=forms.TextInput(attrs={'class': 'form-control'}))
    card_expiry = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'date'}))

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount < 0:
            raise forms.ValidationError("Amount must be greater than 0")
        return amount

class CustomerRegistrationForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))