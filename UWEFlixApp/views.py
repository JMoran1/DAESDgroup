from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView
from .models import MonthlyStatement, Movie

def home(request):
    return render(request, "UWEFlixApp/test.html")

def c_man(request):
    return render(request, "UWEFlixApp/cmanager.html")

def list_movies(request):
    movie_list = Movie.objects.all()
    return render(request, 'UWEFlixApp/view_movies.html', {'movie_list':movie_list})

class ViewMonthlyStatement(ListView):
    model = MonthlyStatement

    def get_context_data(self, **kwargs):
        context = super(ViewMonthlyStatement, self).get_context_data(**kwargs)
        return context