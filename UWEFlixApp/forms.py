from datetime import datetime, timedelta
from math import ceil

from django import forms
from django.contrib import admin
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

from UWEFlixApp.models import Booking, Club, Movie, Screen, Screening, User

from .check_luhn import check_luhn


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
        expiry = datetime.combine(expiry, datetime.min.time())
        if expiry < datetime.now():
            raise forms.ValidationError("Card has expired")
        return expiry


class MinutesDurationField(forms.DurationField):
    def to_python(self, value):
        # current value should be int-like count of minutes, turn it into a timedelta
        return timedelta(minutes=int(value))

    def prepare_value(self, value):
        if isinstance(value, str):  # invalid value, it's now a string --leave as-is
            return value
        # otherwise, it's a timedelta, so format it
        # turns timedelta back into count of minutes
        return str(ceil(value.total_seconds() / 60))  # in unlikely event of seconds, rounds up


class MovieForm(forms.ModelForm):
    running_time = MinutesDurationField(
        initial=timedelta(minutes=1),
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label='Minutes Long',
        validators=[MinValueValidator(limit_value=timedelta(minutes=1))]
    )
    class Meta:
        model = Movie
        fields = ('name', 'running_time', 'rating', 'image')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'minutes_long': forms.TextInput(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'rating': 'BBFC Film Rating (E is "Exempt")'
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

class ScreeningForm(forms.ModelForm):
    class Meta:
        model = Screening
        fields = ('movie', 'screen', 'showing_at')

        widgets = {
            'movie': forms.Select(attrs={'class': 'form-control'}),
            'screen': forms.Select(attrs={'class': 'form-control'}),
            'showing_at': forms.DateTimeInput(attrs={'class': 'form-control'}),
        }

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ('number_of_student_tickets','number_of_child_tickets','number_of_adult_tickets')

    TICKET_OPTIONS = (('0','0'), ('1','1'), ('2','2'), ('3','3'), ('4','4'), ('5','5'), ('6','6'), ('7','7'), ('8','8'), ('9','9'))
    number_of_student_tickets = forms.CharField(label='Number of Student Tickets', help_text = '(Number of attendees)', widget=forms.Select(choices=TICKET_OPTIONS)) 
    
    number_of_child_tickets = forms.CharField(label='Number of Child Tickets', help_text = '(Number of attendees)', widget=forms.Select(choices=TICKET_OPTIONS)) 
    
    number_of_adult_tickets = forms.CharField(label='Number of Adult Tickets', help_text = '(Number of attendees)', widget=forms.Select(choices=TICKET_OPTIONS)) 

    
class ClubTopUpForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.TextInput(attrs={'class': 'form-control'}))
    card_number = forms.CharField(max_length=16, widget=forms.TextInput(attrs={'class': 'form-control'}))
    card_expiry = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'date'}))

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount < 0:
            raise forms.ValidationError("Amount must be greater than 0")
        return amount

class StudentRegistrationForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Confirm Password')

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def clean_username(self):
        if User.objects.filter(username=self.cleaned_data["username"]).exists():
            raise forms.ValidationError("Username already exists")
        return self.cleaned_data["username"]

class ClubRepBookingForm(forms.Form):
    number_of_student_tickets = forms.IntegerField(label='Number of Student Tickets', help_text = '(Number of attendees)', widget=forms.TextInput(attrs={'class': 'form-control'}))

class SimplePaymentForm(forms.Form): #This form will not actually capture any payment information, it will just be used to display the form to the user and to validate the data
    holder_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    card_number = forms.CharField(max_length=16, widget=forms.TextInput(attrs={'class': 'form-control'}))
    card_expiry = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'date'}))
    card_cvv = forms.CharField(max_length=3, widget=forms.TextInput(attrs={'class': 'form-control'}))

    def clean_card_number(self):
        card_number = self.cleaned_data['card_number']
        if not check_luhn(card_number):
            raise forms.ValidationError("Card number is not valid")
        return card_number
    
    def clean_card_expiry(self):
        expiry = self.cleaned_data['card_expiry']
        expiry = datetime.combine(expiry, datetime.min.time())
        if expiry < datetime.now():
            raise forms.ValidationError("Card has expired")
        return expiry
    
class ClubRepRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('club',)

    def clean_club(self):
        if self.cleaned_data['club']:  # truthy, so not blank, fine
            return self.cleaned_data['club']
        else:  # problem, club is mandatory
            raise ValidationError('Club must be specified!')
        
class JoinClubForm(forms.Form):
    club = forms.ModelChoiceField(queryset=Club.objects.all(), blank=False, widget=forms.Select(attrs={'class': 'form-control'}))

class StaffRegistrationForm(forms.ModelForm):
    
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Confirm Password')

    class Meta:
        model = User
        fields = ('role',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].choices = [('M', 'Cinema Manager'), ('A', 'Account Manager')]

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

    def clean_username(self):
        if User.objects.filter(username=self.cleaned_data["username"]).exists():
            raise forms.ValidationError("Username already exists")
        return self.cleaned_data["username"]
    
class TicketPriceForm(forms.Form):
    adult_ticket_price = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.TextInput(attrs={'class': 'form-control'}))
    child_ticket_price = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.TextInput(attrs={'class': 'form-control'}))
    student_ticket_price = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.TextInput(attrs={'class': 'form-control'}))

    def clean_adult_ticket_price(self):
        adult_ticket_price = self.cleaned_data['adult_ticket_price']
        if adult_ticket_price < 0:
            raise forms.ValidationError("Adult ticket price must be greater than 0")
        return adult_ticket_price
    
    def clean_child_ticket_price(self):
        child_ticket_price = self.cleaned_data['child_ticket_price']
        if child_ticket_price < 0:
            raise forms.ValidationError("Child ticket price must be greater than 0")
        return child_ticket_price
    
    def clean_student_ticket_price(self):
        student_ticket_price = self.cleaned_data['student_ticket_price']
        if student_ticket_price < 0:
            raise forms.ValidationError("Student ticket price must be greater than 0")
        return student_ticket_price
