from django.urls import path
from UWEFlixApp import views

urlpatterns = [
    path("", views.home, name="home"),
]