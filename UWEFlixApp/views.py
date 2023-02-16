from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    return render(request, "UWEFlixApp/test.html")

def test(request):
    return HttpResponse("This is a test")