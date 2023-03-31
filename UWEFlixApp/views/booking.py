from django.shortcuts import redirect, render

from UWEFlixApp.forms import BookingForm, ClubRepBookingForm
from UWEFlixApp.models import Booking, Club, Screening, User

def create_booking(request, pk):
    user = request.user
    screening = Screening.objects.get(pk=pk)
    date = Screening.objects.get(pk=pk).showing_at

    screeningtext = screening.id
    warning = None
    request.session['selected_screening'] = screeningtext

    if request.method == 'GET':
        if not user.is_anonymous and user.role == User.Role.CLUB_REP:
            form = ClubRepBookingForm()
            return render(request, "UWEFlixApp/booking_form.html", {"form": form, "button_text": "Continue booking", "user": user, "Screening": screening, 'date': date, 'warning': warning})

    if request.method == 'POST':
        if request.user.is_anonymous or request.user.role != User.Role.CLUB_REP:
            request.session['number_of_adult_tickets'] = request.POST.get(
                'number_of_adult_tickets')

            request.session['number_of_child_tickets'] = request.POST.get(
                'number_of_child_tickets')

            request.session['number_of_student_tickets'] = request.POST.get(
                'number_of_student_tickets')
            total_tickets = int(request.POST.get('number_of_adult_tickets')) + int(request.POST.get(
                'number_of_child_tickets')) + int(request.POST.get('number_of_student_tickets'))
            request.session['total_tickets_number'] = total_tickets
            if screening.seats_remaining < total_tickets:
                warning = "Not enough seats available"
                form = BookingForm()
                return render(request, "UWEFlixApp/booking_form.html", {"form": form, "button_text": "Continue booking", "user": user, "Screening": screening, 'date': date, 'warning': warning})


            else:
                if total_tickets > 9:
                    warning = "Too many tickets, no more than 9 in one booking"
                elif total_tickets == 0:
                    warning = "No tickets selected"
                else:
                    return redirect('confirm_booking')
        else:
            request.session['number_of_student_tickets'] = request.POST.get(
                'number_of_student_tickets')
            request.session['number_of_adult_tickets'] = 0

            request.session['number_of_child_tickets'] = 0

            total_tickets = int(request.POST.get('number_of_student_tickets'))
            print(total_tickets)
            request.session['total_tickets_number'] = total_tickets
            if screening.seats_remaining < total_tickets:
                warning = "Not enough seats available"
                form = ClubRepBookingForm()
                return render(request, "UWEFlixApp/booking_form.html", {"form": form, "button_text": "Continue booking", "user": user, "Screening": screening, 'date': date, 'warning': warning})

            else:
                if total_tickets < 9:
                    warning = "A club booking requirement is 10 tickets or more"
                    form = ClubRepBookingForm()
                    return render(request, "UWEFlixApp/booking_form.html", {"form": form, "button_text": "Continue booking", "user": user, "Screening": screening, 'date': date, 'warning': warning})
                else:
                    return redirect('confirm_booking')

    form = BookingForm()

    return render(request, "UWEFlixApp/booking_form.html", {"form": form, "button_text": "Continue booking", "user": user, "Screening": screening, 'date': date, 'warning': warning})


def confirm_booking(request):

    screening = Screening.objects.get(id=request.session['selected_screening'])

    user = request.user
    # TODO: Change club to be based on the user's club
    if not request.user.is_anonymous and request.user.role == User.Role.CLUB_REP:
        club = Club.objects.get(pk=2)
        discount_rate = club.discount_rate
    discount = None
    number_of_adult_tickets = request.session['number_of_adult_tickets']
    number_of_child_tickets = request.session['number_of_child_tickets']
    number_of_student_tickets = request.session['number_of_student_tickets']
    # screening.seats_remaining = screening.seats_remaining - \
    #     int(number_of_adult_tickets) - int(number_of_child_tickets) - \
    #     int(number_of_student_tickets)
    total_price = int(number_of_adult_tickets) * 4.99 + \
        int(number_of_child_tickets) * 2.99 + \
        int(number_of_student_tickets) * 3.99
    subtotal = total_price
    if not request.user.is_anonymous:
        if user.role == User.Role.CLUB_REP:
            discount = total_price * float(discount_rate)
            total_price = total_price - discount

    total_ticket_quantity = int(number_of_adult_tickets) + \
        int(number_of_child_tickets) + int(number_of_student_tickets)
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if screening.seats_remaining < total_ticket_quantity:
            return render(request, "UWEFlixApp/confirm_booking.html", {"user": user, "Screening": screening, 'number_of_adult_tickets': number_of_adult_tickets, 'number_of_child_tickets': number_of_child_tickets, 'number_of_student_tickets': number_of_student_tickets, 'total_price': total_price, 'subtotal': subtotal, 'discount': discount, 'total_ticket_quantity': total_ticket_quantity, 'button_text': 'Confirm Booking', 'button_texttwo': 'Cancel Booking', 'warning': 'Too many tickets selected'})
        else:
            if request.user.is_authenticated:
                if user.role == User.Role.CLUB_REP:
                    if club.balance < total_price:
                        return render(request, "UWEFlixApp/confirm_booking.html", {"user": user, "Screening": screening, 'number_of_adult_tickets': number_of_adult_tickets, 'number_of_child_tickets': number_of_child_tickets, 'number_of_student_tickets': number_of_student_tickets, 'total_price': total_price, 'subtotal': subtotal, 'discount': discount, 'total_ticket_quantity': total_ticket_quantity, 'button_text': 'Confirm Booking', 'button_texttwo': 'Cancel Booking', 'warning': 'Insufficient funds'})
                    else:
                        Booking.objects.create(user=user, screening=screening, number_of_adult_tickets=number_of_adult_tickets, total_price=total_price,
                                            number_of_child_tickets=number_of_child_tickets, number_of_student_tickets=number_of_student_tickets, club=club)
                        club.balance = float(club.balance) - total_price
                        club.save()
                        screening.seats_remaining = screening.seats_remaining - total_ticket_quantity
                        screening.save()
                else:
                    Booking.objects.create(user=user, screening=screening, number_of_adult_tickets=number_of_adult_tickets, total_price=total_price,
                                    number_of_child_tickets=number_of_child_tickets, number_of_student_tickets=number_of_student_tickets)
                    screening.seats_remaining = screening.seats_remaining - total_ticket_quantity
                    screening.save()
            else:
                Booking.objects.create(screening=screening, number_of_adult_tickets=number_of_adult_tickets, total_price=total_price,
                                    number_of_child_tickets=number_of_child_tickets, number_of_student_tickets=number_of_student_tickets)
                screening.seats_remaining = screening.seats_remaining - total_ticket_quantity
                screening.save()

            return redirect('home')
    else:
        form = BookingForm()

    return render(request, "UWEFlixApp/confirm_booking.html", {"user": user, "Screening": screening, "numtickets": number_of_adult_tickets, 'button_text': 'Confirm Booking', 'button_texttwo': 'Cancel Booking', 'total_price': total_price, 'total_ticket_quantity': total_ticket_quantity, 'discount': discount, 'subtotal': subtotal})
