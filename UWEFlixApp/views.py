from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView
from .models import MonthlyStatement

def home(request):
    return render(request, "UWEFlixApp/test.html")

class ViewMonthlyStatement(ListView):
    model = MonthlyStatement

    def get_context_data(self, **kwargs):
        context = super(ViewMonthlyStatement, self).get_context_data(**kwargs)
        return context