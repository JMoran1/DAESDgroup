from django.urls import path
from UWEFlixApp import views

urlpatterns = [
    path("", views.home, name="home"),
    path("test", views.test, name="test"),
]